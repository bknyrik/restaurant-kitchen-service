import click

from app.extensions import db, bcrypt
from app.database.models.kitchen import CookModel
from app.database.models.users import UserGroupModel, UserGroupEnum


@click.command("create_admin")
@click.argument("username")
@click.argument("password")
def create_admin(username: str, password: str) -> None:
    """Creates admin user."""
    user_exists = (
        db.session
        .query(CookModel.query.filter_by(username=username).exists()
        ).scalar()
    )

    if user_exists:
        print("Admin with this username already exists.")
    else:
        group = (
            db.session.query(UserGroupModel)
            .where(UserGroupModel.name == UserGroupEnum.ADMIN)
            .first()
        )

        db.session.execute(
            db.insert(CookModel)
            .values(
                username=username,
                password=bcrypt.generate_password_hash(password).decode(),
                group_id=group.id
            )
        )
        db.session.commit()

        print(f"Admin {repr(username)} is created.")
