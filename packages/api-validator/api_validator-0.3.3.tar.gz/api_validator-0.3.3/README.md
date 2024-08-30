# OpenAPI Traffic Validator

CLI Tool that validates an OpenAPI specification against a live application using [Newman](https://github.com/postmanlabs/newman). Optionally generates the OpenAPI spec from code using [NightVision](https://www.nightvision.net/).

## Installation

```bash
# pipx is recommended for installing CLI tools
pip install pipx
pipx install api-validator

# Or install it with pip
pip3 install api-validator --user
```

## Usage

First, clone the repository:

```bash
git clone https://github.com/nvsecurity/api-validator.git
cd api-validator
```

### Mode 1: Traffic Validation

* Now run an example app with Docker:

```bash
docker run --restart always -d -p 3000:3000 --name juice-shop bkimminich/juice-shop
```

* Now run the validator to test the API and generate a markdown-formatted report:

```bash
api-validator yolo-traffic \
    --config-file config.yml \
    --swagger-file juice-shop.yml \
    --server http://localhost:3000 \
    --app-name juice-shop
```

It will generate a file called [./summary.md](./summary.md) in the current directory.


### Mode 2: Comparing to existing OpenAPI Specs

You can also compare generated traffic versus an OpenAPI spec. 

* First, list the jobs available in the config file:

```bash
api-validator list-jobs --config-file config.yml
```

It will print out the available jobs in the config file, like this:

<details open>
<summary>Jobs listing</summary>
<br>

```
Language: dotnet, Job Name: altinn-studio, Repo: https://github.com/Altinn/altinn-studio
Language: dotnet, Job Name: bitwarder-server, Repo: https://github.com/bitwarden/server
Language: dotnet, Job Name: dotnet-kavita, Repo: https://github.com/Kareadita/Kavita
Language: dotnet, Job Name: dvcsharp-api, Repo: https://github.com/appsecco/dvcsharp-api
Language: dotnet, Job Name: edwinvw-pitstop-customers, Repo: https://github.com/EdwinVW/pitstop
Language: dotnet, Job Name: edwinvw-pitstop-vehicles, Repo: https://github.com/EdwinVW/pitstop
Language: dotnet, Job Name: edwinvw-pitstop-workshop, Repo: https://github.com/EdwinVW/pitstop
Language: dotnet, Job Name: eshop-catalog-api, Repo: https://github.com/api-extraction-examples/eShop
Language: dotnet, Job Name: eshop-ordering-api, Repo: https://github.com/api-extraction-examples/eShop
Language: dotnet, Job Name: eshop-webhooks-api, Repo: https://github.com/api-extraction-examples/eShop
Language: dotnet, Job Name: featbit, Repo: https://github.com/featbit/featbit
Language: dotnet, Job Name: jellyfin, Repo: https://github.com/NightVisionExamples/jellyfin
Language: dotnet, Job Name: universalis, Repo: https://github.com/Universalis-FFXIV/Universalis
Language: dotnet, Job Name: wallet-wasabi, Repo: https://github.com/zkSNACKs/WalletWasabi
Language: go, Job Name: crAPI-go, Repo: https://github.com/vulnerable-apps/crAPI
Language: js, Job Name: blockchain-explorer, Repo: https://github.com/api-extraction-examples/blockchain-explorer
Language: js, Job Name: cve-services, Repo: https://github.com/api-extraction-examples/cve-services
Language: js, Job Name: dvws-node, Repo: https://github.com/vulnerable-apps/dvws-node
Language: js, Job Name: express-anything-llm, Repo: https://github.com/api-extraction-examples/anything-llm
Language: js, Job Name: express-rest-boilerplate, Repo: https://github.com/dnighvn/express-rest-boilerplate
Language: js, Job Name: hypertube, Repo: https://github.com/api-extraction-examples/Hypertube
Language: js, Job Name: infisicial, Repo: https://github.com/api-extraction-examples/infisical
Language: js, Job Name: juice-shop, Repo: https://github.com/vulnerable-apps/juice-shop
Language: js, Job Name: kubero, Repo: https://github.com/api-extraction-examples/kubero
Language: js, Job Name: nodejs-api-showcase, Repo: https://github.com/api-extraction-examples/nodejs-api-showcase
Language: js, Job Name: nodejs-goof, Repo: https://github.com/vulnerable-apps/nodejs-goof
Language: js, Job Name: valetudo, Repo: https://github.com/api-extraction-examples/Valetudo
Language: python, Job Name: Inventree-django, Repo: https://github.com/api-extraction-examples/InvenTree
Language: python, Job Name: a-flaskrestful-api, Repo: https://github.com/api-extraction-examples/a-flaskrestful-api
Language: python, Job Name: argus-eye-django, Repo: https://github.com/api-extraction-examples/Eye
Language: python, Job Name: cert-viewer-flask, Repo: https://github.com/blockchain-certificates/cert-viewer
Language: python, Job Name: cpa-network-django, Repo: https://github.com/api-extraction-examples/cpa-network
Language: python, Job Name: crAPI-python, Repo: https://github.com/vulnerable-apps/crAPI
Language: python, Job Name: defect-dojo-django, Repo: https://github.com/api-extraction-examples/django-DefectDojo
Language: python, Job Name: django-crm, Repo: https://github.com/api-extraction-examples/Django-CRM
Language: python, Job Name: greater-wms-django, Repo: https://github.com/api-extraction-examples/GreaterWMS
Language: python, Job Name: help-desk-service-django, Repo: https://github.com/api-extraction-examples/help-desk-service
Language: python, Job Name: intelowl-django, Repo: https://github.com/api-extraction-examples/IntelOwl
Language: python, Job Name: karrio-django, Repo: https://github.com/api-extraction-examples/karrio
Language: python, Job Name: librephotos-django, Repo: https://github.com/api-extraction-examples/librephotos
Language: python, Job Name: libretime-django, Repo: https://github.com/api-extraction-examples/libretime
Language: python, Job Name: mathesar-django, Repo: https://github.com/api-extraction-examples/mathesar
Language: python, Job Name: medileaf-backend, Repo: https://github.com/api-extraction-examples/MediLeaf_backend
Language: python, Job Name: netbox-django, Repo: https://github.com/api-extraction-examples/netbox
Language: python, Job Name: nimbler-django, Repo: https://github.com/NimblerSecurity/nimbler-django
Language: python, Job Name: posthog-django, Repo: https://github.com/api-extraction-examples/posthog
Language: python, Job Name: wger-django, Repo: https://github.com/api-extraction-examples/wger
Language: spring, Job Name: Alibaba-Nacos, Repo: https://github.com/api-extraction-examples/nacos
Language: spring, Job Name: Angular-SpringBoot-REST-JWT, Repo: https://github.com/mrin9/Angular-SpringBoot-REST-JWT
Language: spring, Job Name: Netflix-Conductor, Repo: https://github.com/api-extraction-examples/conductor
Language: spring, Job Name: Newbee-Mall, Repo: https://github.com/api-extraction-examples/newbee-mall
Language: spring, Job Name: Spring-boot-Banking, Repo: https://github.com/api-extraction-examples/Spring-boot-Banking
Language: spring, Job Name: ZHENFENG13-My-Blog, Repo: https://github.com/api-extraction-examples/ZHENFENG13-My-Blog
Language: spring, Job Name: apereo-cas, Repo: https://github.com/api-extraction-examples/cas
Language: spring, Job Name: crAPI-spring, Repo: https://github.com/vulnerable-apps/crAPI
Language: spring, Job Name: javaspringvulny, Repo: https://github.com/vulnerable-apps/javaspringvulny
Language: spring, Job Name: thingsboard, Repo: https://github.com/api-extraction-examples/thingsboard
```

</details>


Next, you can choose to run a comparison at different scopes:
1. Select job by job name
2. Bulk select jobs, filtered by language
3. Bulk select all jobs


* Run a comparison for a single job:

```bash
api-validator compare \
    --config-file config.yml \
    --job juice-shop \
    --output-file comparison-juice-shop.md
```

The output will look like this:

<details open>
<summary>Juice Shop output</summary>

```
Thread 0 will process cloning for jobs: juice-shop
	juice-shop/juice-shop: Cloning...
	juice-shop/juice-shop: Local repo already exists. Skipping clone.
juice-shop/juice-shop: Thread 0 progress: Repository cloned for: juice-shop
Thread 0 will process extraction for jobs: juice-shop
	juice-shop/juice-shop: Working on Job: juice-shop
	juice-shop/juice-shop: Repo: https://github.com/juice-shop/juice-shop, Swagger File: https://raw.githubusercontent.com/api-extraction-examples/juice-shop/master/swagger.yml, Language: js
	juice-shop/juice-shop: Downloading base Swagger file...
	juice-shop/juice-shop: Data downloaded from https://raw.githubusercontent.com/api-extraction-examples/juice-shop/master/swagger.yml and saved as /Users/kinnaird/github.com/nvsecurity/api-validator/analysis/base/juice-shop.yml
	juice-shop/juice-shop: Running extraction...
		juice-shop/juice-shop: Running command: api-excavator --log-level info --output /Users/kinnaird/github.com/nvsecurity/api-validator/analysis/revision/juice-shop.yml -l js /Users/kinnaird/github.com/nvsecurity/api-validator/analysis/repos/juice-shop
		juice-shop/juice-shop: INFO Initializing language provider
		juice-shop/juice-shop: INFO Finished initializing language provider
		juice-shop/juice-shop: INFO Starting language provider execution
		juice-shop/juice-shop: ERRO Failed to interpret import { calculateCheatScore, calculateFindItCheatScore, calculateFixItCheatScore } from './antiCheat' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { retrieveCodeSnippet } from '../routes/vulnCodeSnippet' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { calculateCheatScore, calculateFindItCheatScore, calculateFixItCheatScore } from './antiCheat' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginAdminInstruction } from './challenges/loginAdmin' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginAdminInstruction } from './challenges/loginAdmin' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { DomXssInstruction } from './challenges/domXss' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginAdminInstruction } from './challenges/loginAdmin' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { DomXssInstruction } from './challenges/domXss' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ScoreBoardInstruction } from './challenges/scoreBoard' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginAdminInstruction } from './challenges/loginAdmin' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { DomXssInstruction } from './challenges/domXss' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ScoreBoardInstruction } from './challenges/scoreBoard' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PrivacyPolicyInstruction } from './challenges/privacyPolicy' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginAdminInstruction } from './challenges/loginAdmin' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { DomXssInstruction } from './challenges/domXss' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ScoreBoardInstruction } from './challenges/scoreBoard' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PrivacyPolicyInstruction } from './challenges/privacyPolicy' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginJimInstruction } from './challenges/loginJim' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginAdminInstruction } from './challenges/loginAdmin' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { DomXssInstruction } from './challenges/domXss' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ScoreBoardInstruction } from './challenges/scoreBoard' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PrivacyPolicyInstruction } from './challenges/privacyPolicy' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginJimInstruction } from './challenges/loginJim' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ViewBasketInstruction } from './challenges/viewBasket' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginAdminInstruction } from './challenges/loginAdmin' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { DomXssInstruction } from './challenges/domXss' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ScoreBoardInstruction } from './challenges/scoreBoard' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PrivacyPolicyInstruction } from './challenges/privacyPolicy' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginJimInstruction } from './challenges/loginJim' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ViewBasketInstruction } from './challenges/viewBasket' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ForgedFeedbackInstruction } from './challenges/forgedFeedback' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginAdminInstruction } from './challenges/loginAdmin' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { DomXssInstruction } from './challenges/domXss' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ScoreBoardInstruction } from './challenges/scoreBoard' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PrivacyPolicyInstruction } from './challenges/privacyPolicy' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginJimInstruction } from './challenges/loginJim' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ViewBasketInstruction } from './challenges/viewBasket' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ForgedFeedbackInstruction } from './challenges/forgedFeedback' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PasswordStrengthInstruction } from './challenges/passwordStrength' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginAdminInstruction } from './challenges/loginAdmin' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { DomXssInstruction } from './challenges/domXss' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ScoreBoardInstruction } from './challenges/scoreBoard' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PrivacyPolicyInstruction } from './challenges/privacyPolicy' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginJimInstruction } from './challenges/loginJim' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ViewBasketInstruction } from './challenges/viewBasket' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ForgedFeedbackInstruction } from './challenges/forgedFeedback' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PasswordStrengthInstruction } from './challenges/passwordStrength' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { BonusPayloadInstruction } from './challenges/bonusPayload' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginAdminInstruction } from './challenges/loginAdmin' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { DomXssInstruction } from './challenges/domXss' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ScoreBoardInstruction } from './challenges/scoreBoard' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PrivacyPolicyInstruction } from './challenges/privacyPolicy' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginJimInstruction } from './challenges/loginJim' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ViewBasketInstruction } from './challenges/viewBasket' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ForgedFeedbackInstruction } from './challenges/forgedFeedback' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PasswordStrengthInstruction } from './challenges/passwordStrength' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { BonusPayloadInstruction } from './challenges/bonusPayload' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginBenderInstruction } from './challenges/loginBender' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginAdminInstruction } from './challenges/loginAdmin' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { DomXssInstruction } from './challenges/domXss' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ScoreBoardInstruction } from './challenges/scoreBoard' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PrivacyPolicyInstruction } from './challenges/privacyPolicy' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginJimInstruction } from './challenges/loginJim' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ViewBasketInstruction } from './challenges/viewBasket' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ForgedFeedbackInstruction } from './challenges/forgedFeedback' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PasswordStrengthInstruction } from './challenges/passwordStrength' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { BonusPayloadInstruction } from './challenges/bonusPayload' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginBenderInstruction } from './challenges/loginBender' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { TutorialUnavailableInstruction } from './tutorialUnavailable' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginAdminInstruction } from './challenges/loginAdmin' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { DomXssInstruction } from './challenges/domXss' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ScoreBoardInstruction } from './challenges/scoreBoard' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PrivacyPolicyInstruction } from './challenges/privacyPolicy' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginJimInstruction } from './challenges/loginJim' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ViewBasketInstruction } from './challenges/viewBasket' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ForgedFeedbackInstruction } from './challenges/forgedFeedback' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PasswordStrengthInstruction } from './challenges/passwordStrength' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { BonusPayloadInstruction } from './challenges/bonusPayload' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginBenderInstruction } from './challenges/loginBender' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { TutorialUnavailableInstruction } from './tutorialUnavailable' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { CodingChallengesInstruction } from './challenges/codingChallenges' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginAdminInstruction } from './challenges/loginAdmin' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { DomXssInstruction } from './challenges/domXss' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ScoreBoardInstruction } from './challenges/scoreBoard' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PrivacyPolicyInstruction } from './challenges/privacyPolicy' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginJimInstruction } from './challenges/loginJim' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ViewBasketInstruction } from './challenges/viewBasket' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ForgedFeedbackInstruction } from './challenges/forgedFeedback' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PasswordStrengthInstruction } from './challenges/passwordStrength' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { BonusPayloadInstruction } from './challenges/bonusPayload' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginBenderInstruction } from './challenges/loginBender' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { TutorialUnavailableInstruction } from './tutorialUnavailable' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { CodingChallengesInstruction } from './challenges/codingChallenges' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { AdminSectionInstruction } from './challenges/adminSection' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import {
		juice-shop/juice-shop:   waitForRightUriQueryParamPair,
		juice-shop/juice-shop:   waitInMs,
		juice-shop/juice-shop:   waitForAngularRouteToBeVisited,
		juice-shop/juice-shop:   waitForLogIn
		juice-shop/juice-shop: } from '../helpers/helpers' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { type ChallengeInstruction } from '../' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { AdminSectionInstruction } from './challenges/adminSection' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { CodingChallengesInstruction } from './challenges/codingChallenges' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { AdminSectionInstruction } from './challenges/adminSection' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { TutorialUnavailableInstruction } from './tutorialUnavailable' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { CodingChallengesInstruction } from './challenges/codingChallenges' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { AdminSectionInstruction } from './challenges/adminSection' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginBenderInstruction } from './challenges/loginBender' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { TutorialUnavailableInstruction } from './tutorialUnavailable' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { CodingChallengesInstruction } from './challenges/codingChallenges' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { AdminSectionInstruction } from './challenges/adminSection' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { BonusPayloadInstruction } from './challenges/bonusPayload' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginBenderInstruction } from './challenges/loginBender' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { TutorialUnavailableInstruction } from './tutorialUnavailable' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { CodingChallengesInstruction } from './challenges/codingChallenges' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { AdminSectionInstruction } from './challenges/adminSection' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PasswordStrengthInstruction } from './challenges/passwordStrength' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { BonusPayloadInstruction } from './challenges/bonusPayload' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginBenderInstruction } from './challenges/loginBender' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { TutorialUnavailableInstruction } from './tutorialUnavailable' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { CodingChallengesInstruction } from './challenges/codingChallenges' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { AdminSectionInstruction } from './challenges/adminSection' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ForgedFeedbackInstruction } from './challenges/forgedFeedback' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PasswordStrengthInstruction } from './challenges/passwordStrength' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { BonusPayloadInstruction } from './challenges/bonusPayload' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginBenderInstruction } from './challenges/loginBender' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { TutorialUnavailableInstruction } from './tutorialUnavailable' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { CodingChallengesInstruction } from './challenges/codingChallenges' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { AdminSectionInstruction } from './challenges/adminSection' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ViewBasketInstruction } from './challenges/viewBasket' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ForgedFeedbackInstruction } from './challenges/forgedFeedback' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PasswordStrengthInstruction } from './challenges/passwordStrength' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { BonusPayloadInstruction } from './challenges/bonusPayload' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginBenderInstruction } from './challenges/loginBender' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { TutorialUnavailableInstruction } from './tutorialUnavailable' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { CodingChallengesInstruction } from './challenges/codingChallenges' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { AdminSectionInstruction } from './challenges/adminSection' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginJimInstruction } from './challenges/loginJim' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ViewBasketInstruction } from './challenges/viewBasket' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ForgedFeedbackInstruction } from './challenges/forgedFeedback' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PasswordStrengthInstruction } from './challenges/passwordStrength' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { BonusPayloadInstruction } from './challenges/bonusPayload' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginBenderInstruction } from './challenges/loginBender' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { TutorialUnavailableInstruction } from './tutorialUnavailable' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { CodingChallengesInstruction } from './challenges/codingChallenges' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { AdminSectionInstruction } from './challenges/adminSection' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PrivacyPolicyInstruction } from './challenges/privacyPolicy' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginJimInstruction } from './challenges/loginJim' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ViewBasketInstruction } from './challenges/viewBasket' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ForgedFeedbackInstruction } from './challenges/forgedFeedback' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PasswordStrengthInstruction } from './challenges/passwordStrength' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { BonusPayloadInstruction } from './challenges/bonusPayload' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginBenderInstruction } from './challenges/loginBender' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { TutorialUnavailableInstruction } from './tutorialUnavailable' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { CodingChallengesInstruction } from './challenges/codingChallenges' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { AdminSectionInstruction } from './challenges/adminSection' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ScoreBoardInstruction } from './challenges/scoreBoard' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PrivacyPolicyInstruction } from './challenges/privacyPolicy' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginJimInstruction } from './challenges/loginJim' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ViewBasketInstruction } from './challenges/viewBasket' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ForgedFeedbackInstruction } from './challenges/forgedFeedback' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PasswordStrengthInstruction } from './challenges/passwordStrength' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { BonusPayloadInstruction } from './challenges/bonusPayload' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginBenderInstruction } from './challenges/loginBender' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { TutorialUnavailableInstruction } from './tutorialUnavailable' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { CodingChallengesInstruction } from './challenges/codingChallenges' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { AdminSectionInstruction } from './challenges/adminSection' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { DomXssInstruction } from './challenges/domXss' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ScoreBoardInstruction } from './challenges/scoreBoard' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PrivacyPolicyInstruction } from './challenges/privacyPolicy' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginJimInstruction } from './challenges/loginJim' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ViewBasketInstruction } from './challenges/viewBasket' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { ForgedFeedbackInstruction } from './challenges/forgedFeedback' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { PasswordStrengthInstruction } from './challenges/passwordStrength' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { BonusPayloadInstruction } from './challenges/bonusPayload' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { LoginBenderInstruction } from './challenges/loginBender' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { TutorialUnavailableInstruction } from './tutorialUnavailable' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { CodingChallengesInstruction } from './challenges/codingChallenges' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: ERRO Failed to interpret import { AdminSectionInstruction } from './challenges/adminSection' with error runtime error: invalid memory address or nil pointer dereference
		juice-shop/juice-shop: INFO Finished language provider execution
		juice-shop/juice-shop: INFO Starting generating OpenAPI document
		juice-shop/juice-shop: INFO OpenAPI document generated in 653.800208ms
		juice-shop/juice-shop: Number of discovered paths: 87
		juice-shop/juice-shop: Number of discovered classes: 0
		juice-shop/juice-shop: INFO Generated the OpenAPI document.
		juice-shop/juice-shop: INFO Successfully validated the output.
	juice-shop/juice-shop: Performing OASDiff operation...
	Running oasdiff command:
		oasdiff diff /Users/kinnaird/github.com/nvsecurity/api-validator/analysis/base/juice-shop.yml /Users/kinnaird/github.com/nvsecurity/api-validator/analysis/revision/juice-shop.yml --exclude-elements description,examples,title,summary
	juice-shop/juice-shop: Completed work on Job: juice-shop

juice-shop/juice-shop: Thread 0 progress: Completed: juice-shop
Thread 0 final status: Completed: juice-shop
All threads completed.
Saved comparison-juice-shop.md
```

<br>

</details>

* Run a comparison for Python apps:

```bash
api-validator compare \
    --config-file config.yml \
    --language python \
    --output-file comparison-python.md
```

See the example file here: [comparison-python.md](./comparison-python.md).

* Run a comparison for all jobs:

```bash
api-validator compare \
    --config-file config.yml \
    --all \
    --output-file comparison-all.md
```

See the example file here: [comparison-all.md](./comparison-all.md).

* You can also change the binary used to run the tests:

```bash
export API_EXCAVATOR_PATH=/path/to/api-excavator
```

By default, it looks for a binary called `api-extractor` in the current directory.

## Config File

The config file is a YAML file that contains details about the applications you are scanning. For example, you might want to skip certain endpoints that are destructive or that you don't want to test. You should also specify the GitHub repository URL and language of the application; that information is used in the generated Markdown report, but it's not the end of the world if you don't include it.

Here is an example:

```yaml
apps:
  nodejs-goof:
    repo: 'https://github.com/vulnerable-apps/nodejs-goof'
    language: js
    github_stars: 485
    provided_swagger_file: ""
    skip_endpoints:
    - path: '/destroy/:id'
      method: GET
      description: Destroy an endpoint
  juice-shop:
    repo: 'https://github.com/vulnerable-apps/juice-shop'
    language: js
    provided_swagger_file: "https://raw.githubusercontent.com/api-extraction-examples/juice-shop/master/swagger.yml"
    github_stars: 8900
    skip_endpoints:
      - path: '/file-upload'
        method: POST
        description: Upload a file
      - path: '/profile/image/file'
        method: POST
        description: Upload a file
```

## Subcommands

You can split it up into smaller parts too:

```bash
# Install prerequisites
api-validator install

# Extract an API with NightVision
api-validator generate \
  --server https://api.example.com \
  --output openapi-spec.yml

# Convert from OpenAPI to Postman collection
api-validator convert \
  --server http://localhost:3000 \
  --swagger-file examples/nv-juice-shop.yml \
  --postman-file examples/collection.json

# Skip postman request
api-validator exclude postman-request \
  --postman-file examples/collection.json \
  --config-file examples/config.yml \
  --app-name juice-shop

# Run newman
api-validator validate \
  --postman-file examples/collection.json \
  --output-dir examples/newman-data \
  --app-name juice-shop

# Generate a markdown report
api-validator report \
  --data-dir examples/newman-data \
  --output-file examples/juice-shop-summary.md \
  --config-file examples/config.yml
```
