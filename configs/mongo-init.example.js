db = db.getSiblingDB('*{DB__NAME}');

db.createUser({
  user: '*{DB__USER}',
  pwd: '*{DB__PASSWORD}',
  roles: [
    {
      role: 'readWrite',
      db: '*{DB__NAME}',
    },
  ],
});
