import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime
from sim_schema import (
    NocParams,
    SimulationRun,
    SimulationSummary,
    save_as_directory,
    load_from_directory,
)


class TestNocParams:
    """Test suite for NocParams model."""

    def test_noc_params_creation(self):
        """Test basic NocParams creation with all required fields."""
        params = NocParams(
            size=(2, 2),
            buffer_size=4,
            activity_thresh=10,
            injection_rate_numerator=1,
            injection_rate_denominator=10,
            resistive_noise_threshold=5,
            inductive_noise_threshold=10,
        )
        assert params.size == (2, 2)
        assert params.buffer_size == 4
        assert params.activity_thresh == 10
        assert params.injection_rate_numerator == 1
        assert params.injection_rate_denominator == 10
        assert params.resistive_noise_threshold == 5
        assert params.inductive_noise_threshold == 10

    def test_noc_params_with_extra_fields(self):
        """Test that NocParams allows extra fields due to ConfigDict(extra='allow')."""
        params = NocParams(
            size=(3, 3),
            buffer_size=8,
            activity_thresh=20,
            injection_rate_numerator=2,
            injection_rate_denominator=100,
            resistive_noise_threshold=15,
            inductive_noise_threshold=20,
            custom_field="custom_value",
            another_field=42,
        )
        assert params.custom_field == "custom_value"
        assert params.another_field == 42

    def test_noc_params_missing_required_field(self):
        """Test that NocParams raises error when required fields are missing."""
        with pytest.raises(ValueError):
            NocParams(
                size=(2, 2),
                buffer_size=4,
                activity_thresh=10,
                # Missing injection_rate_numerator and other required fields
            )


class TestSimulationRun:
    """Test suite for SimulationRun model."""

    @pytest.fixture
    def basic_simulation_run(self):
        """Fixture providing a basic SimulationRun instance."""
        return SimulationRun(
            noc_parameters={
                "size": (2, 2),
                "buffer_size": 4,
                "injection_rate": 0.1,
            },
            noc_model_file="model content here",
            modest_command="mcsta test.modest",
            raw_modest_output="output from modest",
            verification_time_sec=15.5,
            properties={"prop": 0.5},
            verification_type="mcsta-CTL",
            clock_cycle_bounds=(0, 100),
        )

    def test_simulation_run_creation(self, basic_simulation_run):
        """Test basic SimulationRun creation."""
        run = basic_simulation_run
        assert run.verification_time_sec == 15.5
        assert run.verification_type == "mcsta-CTL"
        assert run.clock_cycle_bounds == (0, 100)

    def test_simulation_run_verification_types(self):
        """Test that all valid verification types are accepted."""
        valid_types = ["mcsta-CTL", "mcsta-PMC", "modes"]
        for vtype in valid_types:
            run = SimulationRun(
                noc_parameters={},
                noc_model_file="model",
                modest_command="cmd",
                raw_modest_output="output",
                verification_time_sec=1.0,
                properties={"prop": 0.0},
                verification_type=vtype,
                clock_cycle_bounds=(0, 50),
            )
            assert run.verification_type == vtype

    def test_simulation_run_invalid_verification_type(self):
        """Test that invalid verification types are rejected."""
        with pytest.raises(ValueError):
            SimulationRun(
                noc_parameters={},
                noc_model_file="model",
                modest_command="cmd",
                raw_modest_output="output",
                verification_time_sec=1.0,
                properties={"prop": 0.0},
                verification_type="invalid-type",
                clock_cycle_bounds=(0, 50),
            )

    def test_simulation_run_serialization(self, basic_simulation_run):
        """Test that SimulationRun can be serialized to dict."""
        run_dict = basic_simulation_run.model_dump()
        assert isinstance(run_dict, dict)
        assert "start_time" not in run_dict
        assert run_dict["verification_time_sec"] == 15.5


class TestSimulationSummary:
    """Test suite for SimulationSummary model."""

    @pytest.fixture
    def sample_runs(self):
        """Fixture providing sample SimulationRun instances."""
        return [
            SimulationRun(
                noc_parameters={"size": (2, 2), "buffer_size": 4},
                noc_model_file=f"model {i}",
                modest_command=f"cmd {i}",
                raw_modest_output=f"output {i}",
                verification_time_sec=10.0 + i,
                properties={"index": i},
                verification_type="mcsta-CTL",
                clock_cycle_bounds=(0, 50),
            )
            for i in range(3)
        ]

    def test_simulation_summary_creation(self, sample_runs):
        """Test basic SimulationSummary creation."""
        summary = SimulationSummary(
            title="Test Summary",
            sub_runs=sample_runs,
            total_time_sec=35.0,
        )
        assert summary.title == "Test Summary"
        assert len(summary.sub_runs) == 3
        assert summary.total_time_sec == 35.0

    def test_simulation_summary_empty_sub_runs(self):
        """Test SimulationSummary with empty sub_runs list."""
        summary = SimulationSummary(
            title="Empty Summary",
            sub_runs=[],
            total_time_sec=0.0,
        )
        assert len(summary.sub_runs) == 0
        assert summary.total_time_sec == 0.0


class TestSaveAndLoadDirectory:
    """Test suite for save_as_directory and load_from_directory functions."""

    @pytest.fixture
    def temp_dir(self):
        """Fixture providing a temporary directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def sample_summary(self):
        """Fixture providing a sample SimulationSummary."""
        runs = [
            SimulationRun(
                noc_parameters={"size": (2, 2), "buffer_size": 4},
                noc_model_file="process noc { ... }",
                modest_command="mcsta -m test.modest",
                raw_modest_output="Result: 0.95",
                verification_time_sec=12.5,
                properties={"pctl_result": 0.95},
                verification_type="mcsta-CTL",
                clock_cycle_bounds=(0, 100),
            ),
            SimulationRun(
                noc_parameters={"size": (3, 3), "buffer_size": 8},
                noc_model_file="process noc3x3 { ... }",
                modest_command="mcsta -m test3x3.modest",
                raw_modest_output="Result: 0.97",
                verification_time_sec=18.3,
                properties={"pctl_result": 0.97},
                verification_type="mcsta-PMC",
                clock_cycle_bounds=(0, 150),
            ),
        ]
        return SimulationSummary(
            title="NoC Verification Suite",
            sub_runs=runs,
            total_time_sec=30.8,
        )

    def test_save_as_directory_creates_structure(self, sample_summary, temp_dir):
        """Test that save_as_directory creates correct directory structure."""
        result_dir = save_as_directory(sample_summary, temp_dir)
        
        # Check main directory exists
        assert result_dir.exists()
        assert result_dir.is_dir()
        
        # Check summary.json exists
        assert (result_dir / "summary.json").exists()
        
        # Check sub-run directories exist (now named run_0, run_1)
        assert (result_dir / "run_0").exists()
        assert (result_dir / "run_1").exists()
        
        # Check files in sub-run directories
        for run_idx in [0, 1]:
            run_dir = result_dir / f"run_{run_idx}"
            assert (run_dir / "metadata.json").exists()
            assert (run_dir / "noc_model.modest").exists()
            assert (run_dir / "modest_output.txt").exists()

    def test_save_creates_valid_json(self, sample_summary, temp_dir):
        """Test that saved JSON files are valid and contain expected data."""
        result_dir = save_as_directory(sample_summary, temp_dir)
        
        # Load and validate summary.json
        with open(result_dir / "summary.json", 'r') as f:
            summary_json = json.load(f)
        
        assert summary_json["title"] == "NoC Verification Suite"
        assert summary_json["total_time_sec"] == 30.8
        assert len(summary_json["sub_run_dirs"]) == 2

    def test_save_preserves_file_contents(self, sample_summary, temp_dir):
        """Test that saved file contents match original data."""
        result_dir = save_as_directory(sample_summary, temp_dir)
        
        # Check first run's files
        run0_model = (result_dir / "run_0" / "noc_model.modest").read_text()
        assert run0_model == "process noc { ... }"
        
        run0_output = (result_dir / "run_0" / "modest_output.txt").read_text()
        assert run0_output == "Result: 0.95"
        
        # Check second run's files
        run1_model = (result_dir / "run_1" / "noc_model.modest").read_text()
        assert run1_model == "process noc3x3 { ... }"

    def test_load_from_directory_recovers_data(self, sample_summary, temp_dir):
        """Test that load_from_directory recovers original SimulationSummary."""
        # Save the summary
        result_dir = save_as_directory(sample_summary, temp_dir)
        
        # Load it back
        loaded_summary = load_from_directory(result_dir)
        
        # Verify structure
        assert loaded_summary.title == sample_summary.title
        assert len(loaded_summary.sub_runs) == len(sample_summary.sub_runs)
        assert loaded_summary.total_time_sec == sample_summary.total_time_sec

    def test_load_recovers_run_details(self, sample_summary, temp_dir):
        """Test that loaded runs match original runs."""
        result_dir = save_as_directory(sample_summary, temp_dir)
        loaded_summary = load_from_directory(result_dir)
        
        # Compare original and loaded runs
        for original, loaded in zip(sample_summary.sub_runs, loaded_summary.sub_runs):
            assert loaded.verification_time_sec == original.verification_time_sec
            assert loaded.verification_type == original.verification_type
            assert loaded.noc_model_file == original.noc_model_file
            assert loaded.raw_modest_output == original.raw_modest_output
            assert loaded.modest_command == original.modest_command
            assert loaded.clock_cycle_bounds == original.clock_cycle_bounds

    def test_roundtrip_save_and_load(self, sample_summary: SimulationSummary, temp_dir):
        """Test complete roundtrip: save then load produces identical data."""
        # Save
        result_dir = save_as_directory(sample_summary, temp_dir)
        
        # Load
        loaded_summary = load_from_directory(result_dir)
        
        # Verify complete equivalence
        assert loaded_summary.model_dump_json() == sample_summary.model_dump_json()

    def test_special_characters_in_title(self, temp_dir):
        """Test that titles with special characters are sanitized."""
        runs = [
            SimulationRun(
                noc_parameters={},
                noc_model_file="model",
                modest_command="cmd",
                raw_modest_output="output",
                verification_time_sec=1.0,
                properties={"ok": True},
                verification_type="mcsta-CTL",
                clock_cycle_bounds=(0, 50),
            )
        ]
        summary = SimulationSummary(
            title="Summary with / special \\ characters",
            sub_runs=runs,
            total_time_sec=1.0,
        )
        
        # Should not raise an exception
        result_dir = save_as_directory(summary, temp_dir)
        assert result_dir.exists()
        
        # Should be able to load it back
        loaded = load_from_directory(result_dir)
        assert len(loaded.sub_runs) == 1

    def test_large_model_content(self, temp_dir):
        """Test saving and loading with large model file content."""
        large_content = "process { " + ("x := x + 1; " * 10000) + "}"
        
        runs = [
            SimulationRun(
                noc_parameters={},
                noc_model_file=large_content,
                modest_command="cmd",
                raw_modest_output="output",
                verification_time_sec=1.0,
                properties={"prop": 0.0},
                verification_type="mcsta-CTL",
                clock_cycle_bounds=(0, 50),
            )
        ]
        summary = SimulationSummary(
            title="Large Content Summary",
            sub_runs=runs,
            total_time_sec=1.0,
        )
        
        result_dir = save_as_directory(summary, temp_dir)
        loaded = load_from_directory(result_dir)
        
        assert loaded.sub_runs[0].noc_model_file == large_content


class TestDataConsistency:
    """Test suite for data consistency and edge cases."""

    def test_noc_parameters_flexibility(self):
        """Test that noc_parameters can contain various data types."""
        params_dict = {
            "size": (2, 2),
            "buffer_size": 4,
            "rates": [0.1, 0.2, 0.3],
            "config": {"key": "value"},
            "enabled": True,
            "timeout": None,
        }
        run = SimulationRun(
            noc_parameters=params_dict,
            noc_model_file="model",
            modest_command="cmd",
            raw_modest_output="output",
            verification_time_sec=1.0,
            properties={"prob": 0.1, "flag": True},
            verification_type="mcsta-CTL",
            clock_cycle_bounds=(0, 50),
        )
        
        assert run.noc_parameters == params_dict
