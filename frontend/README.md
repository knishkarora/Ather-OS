# Ather OS Frontend

The frontend is a React and Vite workflow workspace styled with Tailwind CSS.
It supports browser-memory draft editing, local workflow submission, status
polling, an append-ordered event trace, and explicit recovery for unfinished
workflows.

Run it from this directory:

```powershell
npm run dev
```

Then open the local address printed by Vite (normally `http://localhost:5173`).
Use `npm run build` to create a production build in `dist/`.

The backend must be running on `http://127.0.0.1:8000` before using **Run
workflow** or **Recover**. Recovery follows at-least-once semantics: a task
interrupted after starting may run again. See [[../docs/Frontend Delivery Plan|Frontend Delivery Plan]] and [[../docs/UI Direction|UI Direction]].
