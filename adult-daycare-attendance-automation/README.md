# Adult Day Care — Attendance Extraction & Reporting Automation

## The problem

At an adult day care center, monthly attendance was tracked manually. Each participant had
their own folder in Google Drive containing a Word timesheet, and someone had to open every
document one at a time, read the table, and tally which days each person attended. With
dozens of participants, this was hours of work every month and it was error-prone — a
misread cell meant an inaccurate record for a person whose care and billing depended on it.

I built a tool that reads every participant's timesheet, classifies attendance per day, and
produces a single consolidated Excel report.

## What it does

1. **Mounts Google Drive** and walks the `Individual Timesheets/` directory, one subfolder
   per participant
2. **Verifies file existence first** — before parsing anything, it checks that the named
   timesheet exists in every participant folder and reports which folders are missing it
3. **Parses the docx tables** using `python-docx`, extracting date and time-entry cells
4. **Classifies each date** as Attended or Not Attended based on whether a valid time entry
   is present
5. **Aggregates** all participants into a single DataFrame, filling gaps as Not Attended
6. **Exports to Excel**, auto-naming the file from the month and year in the data
   (`October_2023_Attendance.xlsx`)
7. **Saves back to Drive**, checking for an existing file of the same name and prompting
   before overwriting

## Design decisions

**Check before parsing, then ask.** The original version failed partway through when a
folder was missing its timesheet. Now the script does a full existence pass first, shows
the user exactly which participants are missing files, and asks whether to proceed anyway.
In practice some participants genuinely hadn't submitted yet, so hard-failing was wrong —
but silently skipping them would have produced a quietly incomplete report. Surfacing the
list and letting the user decide was the right middle ground.

**Attendance is inferred from time entries, not a checkbox.** The timesheets record clock
times rather than a yes/no field. A date counts as attended if the corresponding cell
starts with a digit. Dates are validated with `strptime` and skipped if malformed, since
the source documents were hand-edited and inconsistently formatted.

**Never overwrite silently.** Saving checks the destination folder first and requires
explicit confirmation before replacing an existing month's file. These are records the
organization depends on; an accidental overwrite is worse than a failed save.

**Written for non-technical users.** The tool ships with a `Tutorial.ipynb` walkthrough and
prompts in plain language throughout, because the people running it monthly were care staff,
not developers.

## Files

| File | Purpose |
|---|---|
| `Automatic Monthly Attendance Data Extraction and Management Tool.ipynb` | Main tool |
| `Attendance Insights Extractor from Excel Files.ipynb` | Analysis over exported attendance data |
| `Automated File Management for Participant Folders.ipynb` | Bulk participant folder setup and maintenance |
| `Tutorial.ipynb` | Step-by-step guide for non-technical staff |

## Limitations

- **Tightly coupled to one folder structure.** Paths to `Individual Timesheets/` and
  `Monthly Attendance/` are hardcoded. Parameterizing them would make it reusable.
- **Assumes the timesheet table is `doc.tables[0]`.** A document with a header table or
  reordered content would break it.
- **Colab-dependent.** Uses `google.colab.drive` for mounting; running outside Colab would
  need the Drive API or a local sync folder.
- **No logging.** Failures print to console and vanish. For something producing records
  people rely on, a written audit log of what was parsed and what was skipped would be the
  next addition.

## Running it

Built for Google Colab.

```
!pip install python-docx
```

Expects this Drive structure:

```
My Drive/
├── Individual Timesheets/
│   ├── <Participant Name>/
│   │   └── <Month-Year> Participant Timesheet.docx
│   └── ...
└── Monthly Attendance/
```

Run the notebook, enter the timesheet filename when prompted, and the consolidated Excel
report is written to `Monthly Attendance/`.

## Stack

Python, pandas, python-docx, Google Colab / Google Drive
