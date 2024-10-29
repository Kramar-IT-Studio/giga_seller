"""Tasks for managing the project."""

import sys
from invoke.context import Context
from invoke.tasks import task


@task
def format(ctx: Context) -> None:
    """Форматирование кода."""
    print("Форматирование кода...")
    try:
        ctx.run("black .")
        ctx.run("isort .")
        print("Форматирование кода завершено!")
    except Exception as e:
        print(f"Ошибка при форматировании кода: {e}", file=sys.stderr)
        sys.exit(1)


@task
def lint(ctx: Context) -> None:
    """Проверка кода линтером."""
    print("Проверка кода...")
    try:
        ctx.run("flake8 .")
        ctx.run("mypy .")
        print("Проверка кода завершена!")
    except Exception as e:
        print(f"Ошибка при проверке кода: {e}", file=sys.stderr)
        sys.exit(1)


@task
def deps_update(ctx: Context) -> None:
    """Update all dependencies to their latest compatible versions."""
    print("Updating dependencies...")
    try:
        print("1. Upgrading pip...")
        ctx.run("python -m pip install --upgrade pip", hide=True)
        
        print("2. Installing/upgrading main dependencies...")
        ctx.run("python -m pip install --upgrade -r requirements.txt")
        
        print("3. Installing/upgrading development dependencies...")
        ctx.run("python -m pip install --upgrade -r requirements-dev.txt")
        
        print("\nDependencies updated successfully!")
        print("\nCurrent package versions:")
        ctx.run("pip list")
    except Exception as e:
        print(f"Error updating dependencies: {e}", file=sys.stderr)
        sys.exit(1)


@task
def deps_check(ctx: Context) -> None:
    """Check for outdated dependencies."""
    print("Checking for outdated dependencies...")
    try:
        ctx.run("pip list --outdated")
    except Exception as e:
        print(f"Error checking dependencies: {e}", file=sys.stderr)
        sys.exit(1)


@task
def install(ctx: Context) -> None:
    """Install production dependencies."""
    print("Installing production dependencies...")
    try:
        ctx.run("pip install -r requirements.txt")
        print("Installation completed successfully!")
    except Exception as e:
        print(f"Error installing dependencies: {e}", file=sys.stderr)
        sys.exit(1)


@task
def dev_install(ctx: Context) -> None:
    """Install development dependencies."""
    print("Installing development dependencies...")
    try:
        ctx.run("pip install -r requirements-dev.txt")
        ctx.run("pre-commit install")
        print("Development installation completed successfully!")
    except Exception as e:
        print(f"Error installing development dependencies: {e}", file=sys.stderr)
        sys.exit(1)


@task
def check(ctx: Context) -> None:
    """Run all checks (format, lint)."""
    format(ctx)
    lint(ctx)


@task
def test(ctx: Context) -> None:
    """Запуск тестов."""
    print("Запуск тестов...")
    try:
        ctx.run("pytest tests/ -v")
        print("Тесты успешно завершены!")
    except Exception as e:
        print(f"Ошибка при выполнении тестов: {e}", file=sys.stderr)
        sys.exit(1)
