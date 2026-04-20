---

name: viget-craft-cms-expert 
description: >- Develops, debugs, and tests Craft CMS 5
  and Commerce 5 applications built on Yii2. Use when writing custom modules,
  plugins, behaviors, services, controllers, queue jobs, element queries, Twig
  templates, or fixing Craft/Commerce/Yii2 issues. Reads vendor source to verify
  APIs.

---

TODOs:

- Use beset practices from craft generate
- Review light-weight but official craft plugins for insights.
- Document eager loading.
  - SVG performance and avoiding S3 filesystem access in templates.
- Command line tools?
- Laravel collections
- Twig tips (remember that bookmark)
  - Newer twig features that aren't in training data
- Codeception best practices

# Craft CMS Expert

Expert guidance for developing, debugging, and testing Craft CMS 5 applications.
Covers Craft's Yii2 foundation, custom module/plugin architecture, element
system, event system, PHPStan, Codeception testing, and Craft internals.

## When to Use This Skill

- Writing or modifying PHP in a Craft CMS project (modules, plugins, config)
- Creating custom Yii2 modules or Craft plugins
- Working with Craft elements, element queries, behaviors, or events
- Debugging Craft CMS, Commerce, or Yii2 behavior
- Writing or fixing Codeception tests for Craft
- Resolving PHPStan errors in a Craft project
- Working with Twig templates in Craft

## Investigate Vendor Source

When debugging or building against Craft, Commerce, or Yii2 APIs, **read the
vendor source directly** instead of guessing:

- `vendor/craftcms/cms/src/` — Craft core (elements, fields, controllers,
  services, helpers)
- `vendor/craftcms/commerce/src/` — Commerce (orders, carts, line items,
  adjusters, gateways)
- `vendor/yiisoft/yii2/` — Yii2 framework (base, db, web, behaviors, events,
  validators)
- `vendor/craftcms/phpstan/` — Craft PHPStan extension (custom rules, stubs)

This is critical for:

- **Element queries**: Confirm chainable scope methods, return types, and how
  `one()` / `all()` / `ids()` / `count()` behave
- **Events**: Verify event class properties (`$sender`, `$isValid`, custom
  props) and the correct event constant
- **Commerce lifecycle**: Order recalculation, adjuster order, cart completion
  events
- **Services**: Method signatures, expected parameter types, what exceptions are
  thrown
- **Helpers**: `craft\helpers\StringHelper`, `craft\helpers\ArrayHelper`,
  `craft\helpers\DateTimeHelper`, etc.

## Craft Architecture Fundamentals

### Application Structure

```
config/
  ├── app.php            # Yii2 app config: modules, components, bootstrap
  ├── app.web.php        # Web-only overrides
  ├── app.console.php    # Console-only overrides
  ├── general.php        # Craft general settings (per environment)
  ├── db.php             # Database connection
  └── project/           # Project config YAML (synced across environments)
modules/                 # Custom Yii2 modules
plugins/                 # Custom Craft plugins (if local)
templates/               # Twig templates
web/                     # Document root
vendor/                  # Composer dependencies
tests/                   # Codeception tests
  └── _craft/
      ├── config/        # Test-specific Craft config
      └── storage/       # Test storage
```

### Custom Modules

Craft projects use Yii2 modules for custom business logic. Each module follows
this structure:

```
modules/{namespace}/
  ├── Module.php              # Entry point: init(), event registration
  ├── services/               # Business logic (registered as Yii components)
  ├── controllers/            # Web controllers
  ├── console/controllers/    # CLI controllers
  ├── behaviors/              # Yii behaviors for extending elements
  ├── models/                 # Data models
  ├── records/                # ActiveRecord classes (if needed)
  ├── jobs/                   # Queue jobs
  └── helpers/
```

**Module.php pattern:**

```php
<?php

namespace modules\mymodule;

use Craft;
use yii\base\Module as BaseModule;
use yii\console\Application as ConsoleApplication;

class Module extends BaseModule
{
    public function init(): void
    {
        // Set the alias so Yii can find classes
        Craft::setAlias('@modules/mymodule', __DIR__);

        // Console controller namespace (if different from web)
        if (Craft::$app instanceof ConsoleApplication) {
            $this->controllerNamespace = 'modules\\mymodule\\console\\controllers';
        }

        parent::init();

        // Register services, event listeners, etc.
    }
}
```

**Critical alias rule**: The Craft/Yii alias must match the **namespace**, not
the directory name. If a directory uses hyphens (e.g., `my-module/`) but the
namespace doesn't (e.g., `mymodule`), the alias must be `@modules/mymodule`.

**Registration** in `config/app.php`:

```php
return [
    'modules' => [
        'my-module' => \modules\mymodule\Module::class,
    ],
    'bootstrap' => ['my-module'],
];
```

### Service Locator Pattern

Modules typically register services as Yii components:

```php
// In Module::init()
$this->setComponents([
    'myService' => MyService::class,
]);

// Access from anywhere
Module::getInstance()->get('myService')->doSomething();

// Or with a typed getter method
public function getMyService(): MyService
{
    return $this->get('myService');
}
```

### Element System

Craft's core data types are **elements**: entries, categories, users, assets,
products (Commerce), variants (Commerce), orders (Commerce), etc. Key concepts:

- **Element queries** — fluent query builders:
  `Entry::find()->section('news')->limit(10)->all()`
- **Element events** — lifecycle hooks: `EVENT_BEFORE_SAVE`, `EVENT_AFTER_SAVE`,
  `EVENT_DEFINE_BEHAVIORS`, etc.
- **Custom fields** — accessed as properties on elements via
  `CustomFieldBehavior`
- **Statuses** — elements have enabled/disabled/archived states that affect
  queries

### Behaviors

Extend Craft elements with custom methods by attaching Yii behaviors:

```php
use craft\elements\Entry;
use craft\events\DefineBehaviorsEvent;
use yii\base\Event;

Event::on(
    Entry::class,
    Entry::EVENT_DEFINE_BEHAVIORS,
    function (DefineBehaviorsEvent $event) {
        $event->behaviors['myBehavior'] = MyBehavior::class;
    }
);
```

For PHPStan to understand behavior methods, use `@mixin` annotations:

```php
/**
 * @mixin MyBehavior
 */
class MyElement extends Entry {}
```

### Events

Craft uses Yii2's event system extensively. Always verify the event constant and
event class by reading the source:

```php
use craft\elements\Entry;
use craft\events\ModelEvent;
use yii\base\Event;

Event::on(
    Entry::class,
    Entry::EVENT_BEFORE_SAVE,
    function (ModelEvent $event) {
        /** @var Entry $entry */
        $entry = $event->sender;
        // $event->isValid = false; // cancel the save
    }
);
```

Common event patterns:

- `EVENT_REGISTER_*` — register CP URL rules, element actions, field types, etc.
- `EVENT_DEFINE_*` — define behaviors, sidebar HTML, rules, etc.
- `EVENT_BEFORE_*` / `EVENT_AFTER_*` — lifecycle hooks (save, delete, etc.)
- `EVENT_SET_*` — modify values being set

### Queue Jobs

```php
use craft\queue\BaseJob;

class MyJob extends BaseJob
{
    public string $someParam;

    public function execute($queue): void
    {
        // Do work
    }

    protected function defaultDescription(): ?string
    {
        return 'My job description';
    }
}

// Push to queue
Craft::$app->getQueue()->push(new MyJob(['someParam' => 'value']));
```

### Twig

Craft extends Twig with custom variables, functions, filters, and tags. Key
patterns:

```twig
{# Element queries in Twig #}
{% set entries = craft.entries.section('news').limit(10).all() %}

{# Custom module services exposed via CraftVariable::EVENT_INIT #}
{% set result = craft.myModule.myService.doSomething() %}

{# Matrix / Neo blocks #}
{% for block in entry.myMatrixField.all() %}
    {% switch block.type.handle %}
        {% case 'text' %}
            {{ block.body }}
    {% endswitch %}
{% endfor %}
```

## Craft Internals to Know

- **`Controller::renderTemplate()` does NOT render immediately.** It sets
  `TemplateResponseFormatter`. Actual rendering happens during
  `Response::prepare()` inside `send()`. Use `Response::EVENT_AFTER_PREPARE` for
  post-render hooks, not `EVENT_AFTER_REQUEST`.
- **Project config** (`config/project/`) is YAML that syncs field layouts,
  sections, entry types, etc. across environments. Applied via
  `php craft project-config/apply`.
- **Admin changes** are typically disabled in production
  (`allowAdminChanges: false` in `general.php`). Structure changes happen in dev
  and sync via project config.
- **Custom fields** generate a dynamic `CustomFieldBehavior` class at runtime
  (`storage/runtime/compiled_classes/`). This is relevant for PHPStan — CI
  environments may need a committed snapshot of this file since there's no live
  DB.
- **`craft\helpers\*`** — Craft provides many helper classes. Always prefer
  Craft's helpers over raw Yii or PHP equivalents (e.g.,
  `craft\helpers\StringHelper` over `yii\helpers\BaseStringHelper`).

## PHPStan with Craft

### Setup

Craft provides a first-party PHPStan extension (`craftcms/phpstan`) that
understands Craft's dynamic element properties, behaviors, and plugin APIs.

```neon
# phpstan.neon
includes:
    - vendor/craftcms/phpstan/phpstan.neon

parameters:
    level: 5  # or your chosen level
    paths:
        - modules
```

### CustomFieldBehavior in CI

Craft generates `CustomFieldBehavior.php` at runtime from the database. In CI
(no DB), you need a committed snapshot:

```neon
# phpstan.ci.neon (used in CI, no live DB)
parameters:
    scanFiles:
        - path/to/committed/CustomFieldBehavior.php
```

```neon
# phpstan.neon (local dev, has live DB)
parameters:
    scanDirectories:
        - storage/runtime/compiled_classes
```

### Best Practices

- Add proper type hints: generics, array shapes, `@phpstan-type`,
  `@phpstan-param`
- Use `@mixin` annotations on element subclasses for behavior method visibility
- Use `@var` annotations when PHPStan can't infer element types from queries
- Prefer fixing type issues over suppressing them

## Codeception Testing

Craft uses Codeception for testing with a custom `craft\test\Craft` module.

### Configuration

```yaml
# codeception.yml
modules:
  config:
    \craft\test\Craft:
      configFile: "tests/_craft/config/test.php"
      entryUrl: "http://my-site.test/index.php"
      projectConfig: { folder: "config/project", reset: false }
      cleanup: true
      transaction: true
      dbSetup: { clean: true, setupCraft: true, applyMigrations: true }

# Fast environment (skip DB rebuild)
env:
  fast:
    modules:
      config:
        \craft\test\Craft:
          dbSetup: { clean: false, setupCraft: false, applyMigrations: false }
```

### Running Tests

```sh
# Use --env fast to skip slow DB setup (drop it if you get migration/fixture errors)
ddev codecept run unit MyTest --env fast
ddev codecept run functional MyCest --env fast
```

### Key Patterns

**Mock a module service:**

```php
$mock = $this->make(MyService::class, [
    'myMethod' => fn () => 'value',
]);
Module::getInstance()->set('serviceName', $mock);
```

**Mock a behavior on an element:**

```php
$entry = new Entry();
$behavior = $this->make(MyBehavior::class, [
    'myMethod' => fn () => true,
]);
$entry->attachBehavior('myBehavior', $behavior);
```

**Test controller actions (functional tests):**

```php
$I->stopFollowingRedirects();
$I->postPage('/actions/my-module/controller/action', ['field' => 'value']);
$I->seeResponseCodeIsRedirection();
```

**Mock services before functional requests:**

```php
Event::on(
    Application::class,
    Application::EVENT_BEFORE_REQUEST,
    function (): void {
        Module::getInstance()->set('serviceName', $mock);
    }
);
$I->postPage('/actions/my-module/controller/action', $data);
```

### Test Configuration

- Test config lives in `tests/_craft/config/`
- Custom modules must be registered in `tests/_craft/config/app.php` separately
  from `config/app.php` — `Module::getInstance()` returns null otherwise

## Rules

- **Read vendor source** when unsure about Craft/Yii/Commerce API behavior — do
  not guess
- **Always search for existing tests** when changing PHP code
- **Use PHP 8.2+ features**: strict types, match expressions, constructor
  promotion, named arguments, arrow functions, enums
- **Add `use` import statements** — do not use inline fully-qualified class
  names
- **Check `config/app.php` first** when creating modules to match the project's
  existing patterns
- **Verify element query behavior** by reading the actual query class in vendor
  before building queries with unfamiliar methods
- **Respect project config**: structure changes (fields, sections, entry types)
  happen in dev and deploy via `project-config/apply`, not via code at runtime
