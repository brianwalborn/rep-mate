# Database

## Creating and applying a migration

1. Change the schema by updating model(s) in `repmate/models/`.

2. Create the migration by running
    ```
    flask db migrate -m "<MIGRATION DESCRIPTION>"
    ```

3. Apply the migration by running
    ```
    flask db upgrade
    ```
