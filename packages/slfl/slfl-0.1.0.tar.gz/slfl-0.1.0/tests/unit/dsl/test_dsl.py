from pathlib import Path
from pytest import MonkeyPatch, fixture
from freezegun import freeze_time
from slfl._dsl import (
    find_tasks_in_module,
    get_memory_dir,
    gen_job_id,
)
from ...example_proj.sample import tasks as sample_tasks


class TestFindTasksInModule:
    @staticmethod
    def test_sample_tasks():
        tasks = find_tasks_in_module(sample_tasks)
        assert len(tasks) == 3
        assert tasks[0].name == "amount_transfered_to_main"
        assert tasks[1].name == "side_account_balance"
        assert tasks[2].name == "transfer_to_savings"


class TestGetMemoryDir:
    @staticmethod
    def test_standard(tmp_path: Path, monkeypatch: MonkeyPatch):
        monkeypatch.chdir(tmp_path)

        memory_dir = get_memory_dir()

        assert memory_dir.name == "memory"
        assert memory_dir.absolute().parent == tmp_path.absolute()


class TestGenJobID:
    @fixture
    @staticmethod
    def mem_dir(tmp_path: Path) -> Path:
        return tmp_path / "memory"

    class TestRelativeTasksPath:
        @fixture
        @staticmethod
        def tasks_file():
            return Path("tasks/sample.py")

        @staticmethod
        @freeze_time("2024-08-24")
        def test_empty_mem(tasks_file: Path, mem_dir: Path):
            job_id = gen_job_id(tasks_file=tasks_file, memory_dir=mem_dir)

            assert job_id == "2024-08-24-sample"

        @staticmethod
        @freeze_time("2024-08-24")
        def test_existing_jobs(tasks_file: Path, mem_dir: Path):
            mem_dir.mkdir(exist_ok=True)
            (mem_dir / "2024-08-24-sample.yaml").touch()
            (mem_dir / "2024-08-24-sample2.yaml").touch()

            job_id = gen_job_id(tasks_file=tasks_file, memory_dir=mem_dir)

            assert job_id == "2024-08-24-sample3"

        @staticmethod
        @freeze_time("2024-08-24")
        def test_multiple_digits(tasks_file: Path, mem_dir: Path):
            mem_dir.mkdir(exist_ok=True)
            n_prev_ids = 13
            for _ in range(n_prev_ids):
                prev_job_id = gen_job_id(tasks_file=tasks_file, memory_dir=mem_dir)
                (mem_dir / f"{prev_job_id}.yaml").touch()

            job_id = gen_job_id(tasks_file=tasks_file, memory_dir=mem_dir)

            assert job_id == f"2024-08-24-sample{n_prev_ids + 1}"
