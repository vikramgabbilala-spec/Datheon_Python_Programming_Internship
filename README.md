# Datheon Python Programming Internship

## Task 3: Automated File Organizer

`organizer.py` sorts files into category folders based on their extensions. It
supports a dry run, optional recursive scanning, collision-safe file names,
and logging for permission and filesystem errors.

### Requirements

- Python 3.9 or newer
- No third-party packages

### Usage

Preview the changes first:

```powershell
python organizer.py "$HOME\Downloads" --dry-run
```

Organize files directly inside a directory:

```powershell
python organizer.py "$HOME\Downloads"
```

To also scan nested directories and move their files into category folders at
the selected directory's root:

```powershell
python organizer.py "$HOME\Downloads" --recursive
```

Files are sorted into `Documents`, `Images`, `Videos`, `Audio`, `Archives`,
`Code`, or `Others`. Existing files are never overwritten; a numbered suffix
is added to colliding names. Symbolic links are skipped.

### Project status

This repository currently contains the Task 3 deliverable. The internship
submission instructions request at least two completed tasks before evaluation;
add another completed task before submitting for credential review.
