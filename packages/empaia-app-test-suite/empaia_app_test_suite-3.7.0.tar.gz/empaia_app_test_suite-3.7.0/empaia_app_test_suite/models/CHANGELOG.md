# 0.7.0

* added indication and procedure tags to case model to support EMP-0105

# 0.6.1

* removed todo due to codecheck fail

# 0.6.0

* added new FHIR models for questionnaires and questionnaire responses
* added new selector and selector taggings models

# 0.5.7

* removed deprecated pydantic v2 types

# 0.5.6

* fixed error in v3 item post validation

# 0.5.5

* added `ScopeQuery` and `ScopeList` model to v3

# 0.5.4

* added `StatisticsPage` model for marketplace

# 0.5.3

* added `Statistics` and `StatisticsList` models for marketplace

# 0.5.2

* added `CaseQuery` model to v3
* updated pydantic settings definition

# 0.5.1

* fix order of datatypes in app ui storage union

# 0.5.0 (and also 0.4.11)

* rework `SlideStorage` models

# 0.4.10

* added optional property `main_storage_address` to `PostClinicalSlide` model

# 0.4.9

* added pixelmap models

# 0.4.8

* removed tag value `HE` from model examples

# 0.4.7

* changed order of strict datatypes in mps configuration model

# 0.4.6

* remove debug print

# 0.4.5

* added option to disable post model validation with pydantic v2

# 0.4.4

* fix for pycodestyle error E721

# 0.4.3

* further pydantic v2 adoptions

# 0.4.2

* upgrade pycodestyle to 2.11.0
* fix minor pycodestyle issues

# 0.4.1

* migrated `example` to `examples` in `Field`
* added validators v3 to annotation queries

# 0.4.0

* support pydantic version 2

# 0.3.26

* changed timestamp to restricted integer

# 0.3.25

* remove unused customer portal app model

# 0.3.24

* updated post models for App Service v3 API
* removed Annotation Service Core models from v3 API

# 0.3.23

* refactored v3 annotation service post models

# 0.3.22

* added resized image model to portal app

# 0.3.21

* minor codestyle change due to black update

# 0.3.20

* removed optional from tag model

# 0.3.19

* added cleanrance filter to public portal app query

# 0.3.18

* v3/examinations.py:
  * added app_id to Scope model (only for returned Scope, not PostScope)
  * added scopes and jobs to ExaminationsQuery

# 0.3.17

* remove ead from v3 job model

# 0.3.16

* updated customer query model

# 0.3.15

* add support for validation status in query

# 0.3.14

* fix PostJob validator

# 0.3.13

* added validation status and error message fields

# 0.3.12

* added query and admin post model for app views

# 0.3.11

* updated job mode and validation

# 0.3.10

* app configs are now mandatory fields and default to empty dict
* `research_only`defaults to false

# 0.3.9

* updated app view model and ui configuration

# 0.3.8

* renamed PortalAppPreview to AppView
* removed redundant ExtendedConfiguration and renamed AppConfig property names

# 0.3.7

* new ExtendedConfiguration model

# 0.3.6

* renamed AppUiState model to AppUiStorage

# 0.3.4

* added AppUiState model

# 0.3.3

* updated app config (global and customer)

# 0.3.2

* updated marketplace models

# 0.3.1

* removed deprecated models (needed for result tree in WBC 1.0) from v3

# 0.3.0

* Refactor ServiceStatus
  * Changes model
  * excluded from api versions (lives on top level, is not part of empaia API specifications)
* Added v3 models
  * changes to examination only containing one app

# 0.2.2

* moved accesstokentools into own utils folder

# 0.2.1

* added missing annotation models to `\v2` folder

# 0.2.0

* Refactoring to serve models for multiple API versions
* Models before preprocessing feature gone to `v1` folder
* Models for Preprocessing apps `/v2` folder
* `access_token_tools` extensions from `0.1.26` are in both versions

# 0.1.26

* re-introduced old `access_token_tools.ceate_token(subject: str ...)`
* added another method `access_token_tools.create_token_from_dict()...)`
