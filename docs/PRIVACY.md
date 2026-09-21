# Text privacy and data flow

The browser sends submitted text to the configured API. In the supplied application,
text and results live in browser state and process memory; there is no database,
account system, persistent server text history, or production text logging. Downloads
and clipboard exports are user-initiated local actions. Closing or clearing the page
is not a guarantee of forensic deletion from memory or the user's device.

The API temporarily retains client IP/timestamp data for bounded rate limiting.
Application request logs use request IDs, known endpoint names, timing, and status.
Model failure logs use task/error codes. Hosting proxies, analytics added by operators,
crash dumps, and monitoring may have different policies and must be reviewed separately.

Models are downloaded from Hugging Face into a disk cache; inference is executed on
the API host. The supplied code does not send submitted text to a hosted model API.
Downloading artifacts still contacts the model host and can use a server-side token.
Never place credentials in `NEXT_PUBLIC_*` values. Do not submit sensitive text to an
untrusted deployment. See [security](../SECURITY.md) for operational controls.
