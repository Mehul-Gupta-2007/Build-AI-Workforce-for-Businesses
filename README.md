# Mend

Mend is a responsive operations console concept for monitoring business workflows, diagnosing failures, reviewing proposed fixes, and retrying failed runs.

## Run locally

```sh
npm install
npm run dev
```

Open the local URL printed by Vite. The app uses React, TypeScript, Vite, React Router, and Lucide icons.

## Demo access

Choose **Create an account** or use any valid email address and a password of at least six characters on the sign-in page. Demo authentication is stored in this browser's local storage. Use the profile control at the bottom of the sidebar to sign out.

## Product areas

- **Overview:** workflow health, run metrics, and recent recovery activity.
- **Workflows:** search, filter, inspect status, and pause or resume seeded workflows.
- **Incidents:** review diagnostic context, proposed transformations, and approve a simulated validation/retry.
- **Run history:** search and filter seeded executions, then inspect an execution trace.
- **Integrations:** connect or disconnect demo integrations; connection state persists locally.
- **Settings:** adjust recovery, approval, notification, and workspace preferences in the demo UI.

The current app is a frontend prototype. Authentication, AI diagnosis, webhook ingestion, provider integrations, persistence beyond the local browser, and real workflow execution require backend services and credentials before production use.

## Checks

```sh
npm run lint
npm run build
```
