from sqlalchemy import text


class DatabaseHandle:
    def __init__(self, database):
        self.database = database

    def commit(self):
        self.database.session.commit()

    def create_entry(self, entry, key):
        sql = text(
            "INSERT INTO entries (entry, key)"
            + "VALUES (:entry, :key)"
            + "RETURNING id;"
        )
        eid = self.database.session.execute(sql, {"entry": entry, "key": key}).first()[
            0
        ]
        return eid

    def add_field(self, eid, field, value):
        sql = text(
            "INSERT INTO fields (owner_id, field, value) VALUES"
            "  (:id, :field, :value);"
        )
        self.database.session.execute(sql, {"id": eid, "field": field, "value": value})

    def get_references(self, reference):
        sql = text("SELECT id, key FROM entries WHERE entry=:reference")
        references = self.database.session.execute(sql, {"reference": reference})

        for eid, key in references:
            yield eid, key

    def get_fields_of(self, eid):
        sql = text("SELECT field, value FROM fields WHERE owner_id=:id")
        fields = self.database.session.execute(sql, {"id": eid})
        reference = dict(fields.fetchall())
        return reference

    def get_id_of(self, key):
        result = text("SELECT id FROM entries WHERE key=:key")
        execution = self.database.session.execute(result, {"key": key})
        eid = execution.scalar()
        return eid

    def delete_fields_of(self, eid):
        sql = text("DELETE FROM fields WHERE owner_id=:id")
        self.database.session.execute(sql, {"id": eid})

    def delete_entry(self, eid):
        sql = text("DELETE FROM entries WHERE id=:id")
        self.database.session.execute(sql, {"id": eid})
        self.database.session.commit()

    def update_fields(self, eid, field, value):
        sql = text(
            "UPDATE fields SET value=:value WHERE owner_id=:eid AND field=:field"
        )
        self.database.session.execute(sql, {"eid": eid, "field": field, "value": value})
        self.database.session.commit()
