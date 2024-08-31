import pytest
from conftext import conftext
from conftext import get_ini_config
from conftext import conf_ini

CONFTEXT_ONLY_GLOBAL = conftext.read_from_file("""
[conftext]
context = development
service = dummy
""")

CONFTEXT_WITH_MODULE_SECTION = conftext.read_from_file("""
[conftext]
context = production
service = dummy

[package.module]
context = development
""")

FILEPATH_DEFAULT_SECTION = "tests/config/package/module/default_section.ini"
FILEPATH_MULTI_SECTION = "tests/config/package/module/multi_section.ini"
FILEPATH_OVERRIDDEN_SECTION = "tests/config/package/module/overridden_section.ini"


def test_get_ini_config_ok(regtest):
    config = get_ini_config(FILEPATH_DEFAULT_SECTION)
    assert config["auth_token"] == "default_section_auth_token"


@pytest.mark.xfail(raises=FileNotFoundError)
def test_get_ini_config_nok():
    get_ini_config("./invalid/path.ini")


def test_get_default_section(regtest):
    config = conf_ini.read_config(FILEPATH_DEFAULT_SECTION)
    print(conf_ini.get_config_section(
        config, CONFTEXT_WITH_MODULE_SECTION["package.module"]), file=regtest)
    print(conf_ini.get_config_section(
        config, CONFTEXT_ONLY_GLOBAL.defaults()), file=regtest)

def test_get_overridden_section():
    config = conf_ini.read_config(FILEPATH_OVERRIDDEN_SECTION)

    assert config["reader"]["address"] == "default_address"
    assert config["reader"]["username"] == "catalog_reader"

    assert config["writer"]["address"] == "default_address"
    assert config["writer"]["username"] == "catalog_writer"

def test_get_multi_section(regtest):
    config = conf_ini.read_config(FILEPATH_MULTI_SECTION)
    print(conf_ini.get_config_section(
        config, CONFTEXT_WITH_MODULE_SECTION["package.module"]), file=regtest)
    print(conf_ini.get_config_section(
        config, CONFTEXT_ONLY_GLOBAL.defaults()), file=regtest)


def test_get_config(regtest):
    config = get_ini_config(
        FILEPATH_MULTI_SECTION,
        CONFTEXT_WITH_MODULE_SECTION["package.module"])
    assert config["auth_token"] == "multi_section_auth_token_development"
