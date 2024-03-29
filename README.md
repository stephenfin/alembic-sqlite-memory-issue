# Demonstration of a possible oslo.db-alembic bug

**Resolution** This wasn't an issue with oslo.db. Instead, we were creating
multiple connections as part of our migration. This doesn't work with in-memory
databases. The final commit in this repo contains the fixes. You can view the
comments from @zzzeek suggesting the fix [here][comments].

There seems to be a weird interaction between oslo.db and alembic. This
demonstrates this. You can validate this with pytest (unittest would also
work). First, create a virtualenv:

```bash
$ virtualenv .venv
$ . .venv
```

Then install the dependencies before running tests:

```
(venv) $ pip install -r requirements.txt
(venv) $ pytest
```

You'll see the test fails and prints the following:

```bash
Expected:
['alembic_version', 'volume_usage_cache']

Actual:
[]
```

However, if I run `alembic upgrade head` using the provided `alembic.ini` then
we see:

```bash
Expected:
['alembic_version', 'volume_usage_cache']

Actual:
['alembic_version', 'volume_usage_cache']
```

We can achieve the same thing using an in-memory database. If we make the
following change:

```diff
diff --git alembic.ini alembic.ini
index 00ee926..fb196bc 100644
--- alembic.ini
+++ alembic.ini
@@ -8,7 +8,7 @@ script_location = %(here)s/foo/migrations
 # defaults to the current working directory.
 prepend_sys_path = .
 
-sqlalchemy.url = sqlite:///foo.db
+sqlalchemy.url = sqlite://
 
 # Logging configuration
 [loggers]
```

Then we also get the following output from `alembic upgrade head`:

```bash
Expected:
['alembic_version', 'volume_usage_cache']

Actual:
[]
```

So this seems to be an issue with context changing and a new in-memory database
being created.

[comments]: https://github.com/stephenfin/alembic-sqlite-memory-issue/commit/28f7d6e814b0751e1f743e0abad680e66102d42b
