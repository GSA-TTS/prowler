from pathlib import Path


class TestCloudgovBuildpackRequirements:
    def test_celery_runtime_includes_redis_client(self):
        requirements_path = Path(__file__).resolve().parents[4] / "requirements.txt"
        requirements = requirements_path.read_text().splitlines()

        assert any(requirement.startswith("redis==") for requirement in requirements)

    def test_web_runtime_includes_uvicorn_gunicorn_worker(self):
        requirements_path = Path(__file__).resolve().parents[4] / "requirements.txt"
        requirements = requirements_path.read_text().splitlines()

        assert "uvicorn-worker==0.4.0" in requirements

    def test_web_runtime_includes_django_eventstream(self):
        requirements_path = Path(__file__).resolve().parents[4] / "requirements.txt"
        requirements = requirements_path.read_text().splitlines()

        assert "django-eventstream==5.3.3" in requirements
        assert "django-grip==3.5.2" in requirements
        assert "gripcontrol==4.4.0" in requirements
        assert "pubcontrol==3.5.0" in requirements

    def test_runtime_prowler_dependency_matches_the_api_lockfile(self):
        requirements_path = Path(__file__).resolve().parents[4] / "requirements.txt"
        requirements = requirements_path.read_text()

        assert "prowler==5.41.0" in requirements
        assert "dulwich==1.2.5" in requirements
        assert "kingfisher-bin==1.104.0" in requirements
        assert "linode-api4==5.45.0" in requirements
        assert "truststore==0.10.4" in requirements
        assert "zstandard==0.25.0" in requirements

    def test_worker_script_uses_cloudgov_safe_celery_defaults(self):
        script_path = Path(__file__).resolve().parents[4] / "bin" / "cloudgov-worker.sh"
        script = script_path.read_text()

        assert '--pool "${CELERY_WORKER_POOL:-solo}"' in script
        assert '--concurrency "${CELERY_WORKER_CONCURRENCY:-1}"' in script

    def test_manifest_allocates_extra_memory_for_beat(self):
        manifest_path = Path(__file__).resolve().parents[5] / "manifest.yml"
        manifest = manifest_path.read_text()

        assert "- name: prowler-api-beat" in manifest
        assert "memory: 512M" in manifest

    def test_web_script_only_runs_migrations_when_enabled(self):
        script_path = Path(__file__).resolve().parents[4] / "bin" / "cloudgov-web.sh"
        script = script_path.read_text()

        assert 'if [[ "${RUN_DB_MIGRATIONS:-0}" == "1" ]]; then' in script
        assert "python manage.py migrate" in script

    def test_manifest_disables_web_boot_migrations(self):
        manifest_path = Path(__file__).resolve().parents[5] / "manifest.yml"
        manifest = manifest_path.read_text()

        assert "RUN_DB_MIGRATIONS: 0" in manifest
