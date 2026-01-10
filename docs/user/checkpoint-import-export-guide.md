# Checkpoint Import/Export Guide

This guide explains how to use the session import and export functionality in the GNS3 Copilot sidebar.

## Feature Overview

GNS3 Copilot now supports exporting and importing sessions directly from the sidebar, allowing you to:

- 📤 **Export Session**: Save the current session to a local file as a backup
- 📥 **Import Session**: Restore a previously exported session from a local file
- 🔄 **Session Migration**: Migrate sessions between different instances or devices

## Using the Export Function

### Step 1: Select a Session

Select the session you want to export from the "Session History" dropdown in the sidebar.

### Step 2: Click the Export Button

Below the "Current Session" information, click the **:material/download: Export** button.

### Step 3: Download the File

After successful export, a download button **:material/download_file: Download File** will appear. Click it to download the file.

### File Naming

The exported file name format is: `{Session Title}_{Timestamp}.json`

Example: `Network_Configuration_20260108_234012.json`

### File Contents

The exported file includes:
- ✅ Complete checkpoint data
- ✅ All messages (including tool_calls)
- ✅ Conversation title
- ✅ Selected GNS3 project
- ✅ Session metadata

## Using the Import Function

### Step 1: Upload a File

In the "**Import Session**" area in the sidebar, click the "**Browse files**" button to select a file.

### Supported File Formats

- `.json` - Recommended format
- `.txt` - Compatible format

### Step 2: Automatic Import

After selecting a file, the system will automatically:
1. Verify the file format
2. Import session data
3. Create a new thread
4. Refresh the session list

### Step 3: View the Imported Session

After successful import, a success message will appear including the new thread ID. You can select the newly imported session from the session history dropdown.

## Use Cases

### Use Case 1: Back Up Important Sessions

```text
1. Select an important session
2. Click the "Export" button
3. Download and save the file to a safe location
```

### Use Case 2: Migrate Between Devices

```text
Device A:
1. Export session → Download file → Transfer file

Device B:
2. Upload file → Import session → Start using
```

### Use Case 3: Restore Accidentally Deleted Sessions

```text
1. Select the exported session from backup file
2. Import to a new thread
3. Continue using the restored session
```

## Frequently Asked Questions

### Q: What data is included in the exported file?

A: The exported file contains the complete session state, including:
- All conversation messages (user, AI, tool calls)
- Conversation title
- Selected GNS3 project
- Session metadata and configuration

### Q: Will importing a session overwrite existing sessions?

A: No. The import function creates a new thread and will not affect existing sessions.

### Q: Do I need to reselect the session after importing?

A: Yes. After successful import, you need to select the newly imported session from the session history dropdown to view and use it.

### Q: Can I import files exported from other versions?

A: You can import any session file exported by GNS3 Copilot. As long as the file format is correct, it can be successfully imported.

### Q: What should I do if import fails?

A: If import fails, the system will display detailed error information. Common reasons include:
- Incorrect file format (must be valid JSON)
- File was not exported by GNS3 Copilot
- File is corrupted

### Q: Will Chinese content be garbled?

A: No. Both export and import use UTF-8 encoding, properly handling Chinese and other multilingual content.

## Best Practices

1. **Regular Backups**: Regularly export important sessions as backups
2. **Naming Convention**: Keep session titles clear for easy identification of exported files
3. **Secure Storage**: Store exported files in secure locations
4. **Verify Imports**: Check session content after import to ensure completeness
5. **Version Compatibility**: Ensure you use the same version of GNS3 Copilot for both import and export

## Technical Details

### File Format

The exported file is in JSON format with the following structure:

```json
{
  "checkpoint": {
    "v": 3,
    "ts": "2026-01-08T23:40:12.123456",
    "id": "checkpoint-id",
    "channel_values": {
      "messages": [...],
      "conversation_title": "...",
      "selected_project": (...)
    },
    "channel_versions": {...},
    "versions_seen": {...},
    "next": null
  },
  "config": {...},
  "metadata": {...}
}
```

### Message Serialization

All messages are serialized to ensure:
- JSON compatibility
- Cross-instance migration
- UI compatibility

### Data Validation

The following are validated during import:
- File format validity
- Data structure integrity
- Message UI compatibility

## Related Documentation

- [User FAQ](FAQ.md)
