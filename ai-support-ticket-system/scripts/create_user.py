"""Create a local agent or admin account without exposing privileged registration."""

import argparse
import asyncio
from getpass import getpass

from sqlalchemy import select

from app.db.database import AsyncSessionLocal
from app.models.user import User, UserRole
from app.services.auth import hash_password


async def create_user(username: str, role: UserRole) -> None:
    password = getpass("Password: ")
    confirmation = getpass("Confirm password: ")
    if password != confirmation:
        raise SystemExit("Passwords do not match.")
    if len(password) < 8:
        raise SystemExit("Password must contain at least 8 characters.")

    async with AsyncSessionLocal() as session:
        existing_user = await session.scalar(select(User).where(User.username == username))
        if existing_user:
            raise SystemExit("That username already exists.")

        session.add(User(username=username, password_hash=hash_password(password), role=role))
        await session.commit()
    print("Created {0} account: {1}".format(role.value, username))


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a local privileged user.")
    parser.add_argument("--username", required=True)
    parser.add_argument("--role", required=True, choices=["agent", "admin"])
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_arguments()
    asyncio.run(create_user(arguments.username, UserRole(arguments.role)))
