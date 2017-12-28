# Run, Build, Deploy

## Quickstart

### I want to develop

| Developing | Dev Script             | Prod Script             |
| :--------- | :--------------------- | :---------------------- |
| Frontend   | `npm run electron`     | |
| Backend    | `npm run electron:dev` | `npm run electron:prod` |

### I want to package

| Platform | Create an Executable | Create an Installer |
| :------- | :------------------- | :------------------ |
| All      | `npm run pack`       | `npm run dist`      |
| Windows  | `npm run pack:win`   | `npm run dist:win`  |
| Mac      | `npm run pack:mac`   | `npm run dist:mac`  |
| Linux    | `npm run pack:lin`   | `npm run dist:lin`  |

### I want to publish the application to Github Releases

Run: `npm run release`

## Package.json Commands

### Scripts

#### ng

> Runs the angular command line.

Executes: `ng`

#### start

> Starts the Angular web server and displays the site.

Executes: `ng serve`

#### build

> Builds the Angular application into static files.

Executes `ng build`

#### build:prod

> Builds the Angular application into static files in production mode.

Executes `ng build --prod`

#### test

> Runs Angular unit tests with Karma.

Executes `ng test`

#### test-ci

> Runs Angular unit tests once with code coverage - for continuous integration.

Executes `ng test --single-run --code-coverage`

#### lint

> Runs tslint to check code for consistency and quality.

Executes `ng lint`

#### e2e

> Runs Angular end-to-end tests with Protractor.

Executes `ng e2e`

#### pack

> Builds the production Angular application then creates the Windows, Mac, and Linux executables.

Executes: `npm run build:prod; electron-builder --dir -wml`

#### pack:win

> Builds the production Angular application then creates the Windows executable.

Executes: `npm run build:prod; electron-builder --dir -w`

#### pack:mac

> Builds the production Angular application then creates the Mac executable.

Executes: `npm run build:prod; electron-builder --dir -m`

#### pack:lin

> Builds the production Angular application then creates the Linux executable.

Executes: `npm run build:prod; electron-builder --dir -l`

#### dist

> Builds the production Angular application then creates the Windows, Mac, and Linux installers.

Executes: `npm run build:prod; electron-builder -wml`

#### dist:win

> Builds the production Angular application then creates the Windows installer.

Executes: `npm run build:prod; electron-builder -w`

#### dist:mac

> Builds the production Angular application then creates the Mac installer.

Executes: `npm run build:prod; electron-builder -m`

#### dist:lin

> Builds the production Angular application then creates the Linux installer.

Executes: `npm run build:prod; electron-builder -l`

#### release

> Builds the production Angular application then creates the Windows, Mac, and Linux installers before uploading a draft release to Github Releases.

Executes: `npm run build:prod; build -wml`

#### electron

> Runs the dynamic development instance of electron.

Executes: `npm run electron:dev:dynamic`

#### electron:dev

> Builds the Angular application then runs the electron application for development.

Executes: `npm run build; electron .`

#### electron:dev:dynamic

> Starts the Angular application webserver and runs the electron application in dynamic mode - this allows the Angular application to be dynamically reloaded during development.

Executes: `concurrently \"npm run start\" \"electron . dynamic\"`

#### electron:prod

> Builds the production Angular application then runs the electron application for development.

Executes: `npm run build:prod; electron .`
