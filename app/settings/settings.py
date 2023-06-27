from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="Qoil_Qliq_app",
    settings_files=["app/settings/settings.default.yaml"],
    environments=True,
    default_env="default",
    env="production",
    merge_enabled=True,
    load_dotenv=False
)
pass