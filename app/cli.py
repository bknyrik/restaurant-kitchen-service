import click

from app.extensions import db, bcrypt
from app.database.models.kitchen import CookModel
from app.database.models.users import UserGroupModel, UserGroupEnum


@click.command("create_admin", help="Create admin user.")
@click.argument("username")
@click.argument("password")
def create_admin(username: str, password: str) -> None:
    try:
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
    except db.SQLAlchemyError as error:
        db.session.rollback()
        print(error)


@click.command("change_password", help="Change user password.")
@click.argument("username")
@click.argument("password")
def change_password(username: str, password: str) -> None:
    try:
        user = (
            db.session
            .query(CookModel)
            .where(CookModel.username == username)
            .first()
        )

        if not user:
            print("User with this username doesn't exist.")
        else:
            user.password = bcrypt.generate_password_hash(password).decode()
            db.session.commit()

            print(
                f"Password for user {repr(username)} "
                f"was changed successfully."
            )
    except db.SQLAlchemyError as error:
        db.session.rollback()
        print(error)
