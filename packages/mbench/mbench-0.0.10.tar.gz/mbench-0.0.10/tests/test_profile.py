import pytest
from unittest.mock import patch, MagicMock
from mbench.profile import FunctionProfiler, profileme, profile, profiling, display_profile_info
import os
import time
from rich.console import Console

console = Console()

@pytest.fixture
def profiler():
    return FunctionProfiler()

def test_load_data(profiler, tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text('Function,Calls,Total Time,Total CPU,Total Memory,Total GPU,Total IO,Avg Duration,Avg CPU Usage,Avg Memory Usage,Avg GPU Usage,Avg IO Usage,Notes\n'
                        'test_func,1,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,\n')
    profiler.csv_file = str(csv_file)
    profiler.load_data()
    assert profiler.profiles['test_func']['calls'] == 1

def test_save_data(profiler, tmp_path):
    csv_file = tmp_path / "test.csv"
    profiler.csv_file = str(csv_file)
    profiler.profiles['test_func'] = {
        'calls': 1,
        'total_time': 1.0,
        'total_cpu': 1.0,
        'total_memory': 1.0,
        'total_gpu': 1.0,
        'total_io': 1.0,
        'notes': ''
    }
    profiler._save_data()  # Changed to _save_data
    content = csv_file.read_text()
    assert 'test_func,1,1.000000,1.000000,1.000000,1.000000,1.000000,1.000000,1.000000,1.000000,1.000000,1.000000,' in content

@pytest.mark.parametrize("mock_used, num_gpus, expected", [
    (1024, 1, 1024),
    (1024, 8, 8192),
    (2048, 1, 2048),
    (2048, 8, 16384),
    (0, 1, 0),
])
def test_get_gpu_usage(profiler, mock_used, num_gpus, expected):
    with patch('pynvml.nvmlDeviceGetMemoryInfo') as mock_nvml, \
         patch.object(profiler, 'num_gpus', num_gpus):
        mock_nvml.return_value.used = mock_used
        total, usages = profiler._get_gpu_usage()
        assert total == expected
        assert len(usages) == num_gpus
        assert all(usage == mock_used for usage in usages)

@pytest.mark.parametrize("read_bytes, write_bytes, expected", [
    (1024, 1024, 2048),
    (0, 1024, 1024),
    (1024, 0, 1024),
    (0, 0, 0),
])
def test_get_io_usage(profiler, read_bytes, write_bytes, expected):
    with patch('psutil.disk_io_counters') as mock_psutil:
        mock_psutil.return_value.read_bytes = read_bytes
        mock_psutil.return_value.write_bytes = write_bytes
        assert profiler._get_io_usage() == (expected, read_bytes, write_bytes)

def test_start_profile(profiler):
    with patch('time.time', return_value=1.0), \
         patch('psutil.virtual_memory', return_value=MagicMock(used=1024)), \
         patch('pynvml.nvmlDeviceGetMemoryInfo', return_value=MagicMock(used=1024)):
        mock_frame = MagicMock()
        mock_frame.f_globals = {'__name__': 'test_module'}
        mock_frame.f_code.co_name = 'test_func'
        profiler.set_target_module('test_module', 'all')
        profiler._start_profile(mock_frame)
        assert profiler.current_calls['test_func']['start_time'] == 1.0

def test_end_profile(profiler):
    profiler.profiles.clear()  # Reset profiles before the test
    with patch('time.time', return_value=2.0), \
         patch('time.process_time', return_value=2.0), \
         patch('psutil.virtual_memory', return_value=MagicMock(used=2048)), \
         patch.object(profiler, '_get_gpu_usage', return_value=(2048, [2048])), \
         patch.object(profiler, '_get_io_usage', return_value=(2048, 1024, 1024)), \
         patch.object(profiler, 'num_gpus', 1):  # Set num_gpus to 1 for this test
        profiler.current_calls['test_func'] = {
            'start_time': 1.0,
            'cpu_start': 1.0,
            'mem_start': 1024,
            'gpu_start': 1024,
            'io_start': 1024
        }
        mock_frame = MagicMock()
        mock_frame.f_globals = {'__name__': 'test_module'}
        mock_frame.f_code.co_name = 'test_func'
        profiler.set_target_module('test_module', 'all')
        profiler._end_profile(mock_frame)
        assert profiler.profiles['test_func']['calls'] == 1
        assert profiler.profiles['test_func']['total_time'] == 1.0
        assert profiler.profiles['test_func']['total_cpu'] == 1.0
        assert profiler.profiles['test_func']['total_memory'] == 1024
        assert profiler.profiles['test_func']['total_gpu'] == 1024
        assert profiler.profiles['test_func']['total_io'] == 1024



@pytest.mark.parametrize("bytes_value, expected", [
    (1024, '1.00 KB'),
    (1024 * 1024, '1.00 MB'),
    (1024 * 1024 * 1024, '1.00 GB'),
    (500, '500.00 B'),
])
def test_format_bytes(profiler, bytes_value, expected):
    assert profiler.format_bytes(bytes_value) == expected

def test_profileme():
    with patch('mbench.profile.FunctionProfiler') as mock_profiler:
        profileme()
        assert mock_profiler.called

def test_profile():
    with patch('mbench.profile.FunctionProfiler') as mock_profiler, \
         patch.dict(os.environ, {'MBENCH': '1'}), \
         patch('mbench.profile._profiler_instance', mock_profiler.return_value):
        mock_instance = mock_profiler.return_value
        mock_instance._get_gpu_usage.return_value = 0
        mock_instance.format_bytes.return_value = "0 B"
        
        @profile
        def test_func():
            pass
        
        test_func()
        
        mock_instance._start_profile.assert_called()
        mock_instance._end_profile.assert_called()
        assert mock_profiler.called

def test_min_duration():
    with patch('mbench.profile.display_profile_info') as mock_display, \
         patch.dict(os.environ, {'MBENCH': '1'}), \
         patch('mbench.profile.FunctionProfiler') as mock_profiler:
        mock_instance = mock_profiler.return_value
        mock_instance._get_gpu_usage.return_value = (0, [0])
        mock_instance._get_io_usage.return_value = (0, 0, 0)
        with profiling("short_block"):
            time.sleep(0.1)
        mock_display.assert_called_once()
        mock_display.reset_mock()

        with profiling("long_block"):
            time.sleep(1.1)
        mock_display.assert_called_once()

def test_quiet_mode():
    with patch('mbench.profile.display_profile_info') as mock_display, \
         patch('mbench.profile.FunctionProfiler') as mock_profiler:
        mock_instance = mock_profiler.return_value
        mock_instance._get_gpu_usage.return_value = (0, [0])
        mock_instance._get_io_usage.return_value = (0, 0, 0)
        with profiling("quiet_block", quiet=True):
            pass
        mock_display.assert_not_called()

def test_summary_mode():
    with patch('mbench.profile.FunctionProfiler') as mock_profiler, \
         patch('mbench.profile.display_profile_info') as mock_display, \
         patch.dict(os.environ, {'MBENCH': '1'}), \
         patch('mbench.profile._profiler_instance', mock_profiler.return_value):
        mock_instance = mock_profiler.return_value
        mock_instance.get_gpu_usage.return_value = (0, [0])
        mock_instance.get_io_usage.return_value = (0, 0, 0)
        mock_instance.format_bytes.return_value = "0 B"
        mock_instance.summary_mode = True
        mock_instance.profiles = {
            'test_func': {
                'calls': 0,
                'total_time': 0,
                'total_cpu': 0,
                'total_memory': 0,
                'total_gpu': 0,
                'total_io': 0,
                'notes': ''
            }
        }
            
        @profile
        def test_func():
            pass

        test_func()
            
        mock_display.assert_called_once()
            
        args, kwargs = mock_display.call_args
        assert 'name' in kwargs
        assert kwargs['name'] == 'test_func'
        assert 'calls' in kwargs
        assert kwargs['calls'] == 1

def test_profiling():
    with patch('mbench.profile.FunctionProfiler') as mock_profiler, \
         patch('mbench.profile._profiler_instance', None), \
         patch.dict(os.environ, {'MBENCH': '1'}), \
         patch('sys._getframe') as mock_getframe:
        mock_instance = mock_profiler.return_value
        mock_instance._get_gpu_usage.return_value = (1024, [1024])
        mock_instance._get_io_usage.return_value = (1024, 512, 512)
        mock_instance.profiles = {
            'test_func': {
                "calls": 1,
                "total_time": 1.0,
                "total_cpu": 1.0,
                "total_memory": 1024,
                "total_gpu": 1024,
                "total_io": 1024,
                "notes": ""
            }
        }
        mock_instance.format_bytes.side_effect = lambda x: f"{x} bytes"
        mock_frame = MagicMock()
        mock_getframe.return_value = mock_frame

        with profiling('test_func'):
            pass

        assert mock_profiler.called
        mock_instance.start_profile.assert_called_once_with(mock_frame)
        mock_instance.end_profile.assert_called_once_with(mock_frame)

def test_display_profile_info():
    with patch('mbench.profile.console.print') as mock_print:
        display_profile_info(
            name="test_func",
            duration=1.0,
            cpu_usage=0.5,
            mem_usage=1024,
            gpu_usage=2048,
            io_usage=4096,
            avg_time=1.0,
            avg_cpu=0.5,
            avg_memory=1024,
            avg_gpu=2048,
            avg_io=4096,
            calls=1
        )
        mock_print.assert_called()

        mock_print.reset_mock()
        display_profile_info(
            name="test_func",
            duration=0.4,
            cpu_usage=0.2,
            mem_usage=512,
            gpu_usage=1024,
            io_usage=2048,
            avg_time=0.4,
            avg_cpu=0.2,
            avg_memory=512,
            avg_gpu=1024,
            avg_io=2048,
            calls=1
        )
        mock_print.assert_called()

        mock_print.reset_mock()
        display_profile_info(
            name="test_func",
            duration=1.0,
            cpu_usage=0.5,
            mem_usage=1024,
            gpu_usage=2048,
            io_usage=4096,
            avg_time=1.0,
            avg_cpu=0.5,
            avg_memory=1024,
            avg_gpu=2048,
            avg_io=4096,
            calls=1
        )
        mock_print.assert_called()
