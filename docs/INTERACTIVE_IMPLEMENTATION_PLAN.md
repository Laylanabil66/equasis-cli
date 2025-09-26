# Equasis CLI Interactive Mode Implementation Plan

## Overview
This document provides a comprehensive plan for implementing interactive mode in the Equasis CLI tool. The interactive mode transforms the traditional command-line interface into a REPL-style interface similar to Claude Code, with slash command syntax and persistent session management.

## Current Status ✅

### Completed Features
- ✅ **Core Interactive Shell**: Created `equasis_cli/interactive.py` with full REPL functionality
- ✅ **Slash Command Parsing**: Implemented `/imo`, `/name`, `/company`, `/format`, `/output` parameter parsing
- ✅ **Session Management**: Persistent authentication and connection handling
- ✅ **Dual-Mode Detection**: Automatically starts interactive mode when no arguments provided
- ✅ **Interactive Help System**: Built-in help for all commands with examples
- ✅ **Command Implementation**: All core commands (vessel, search, fleet) working with slash syntax
- ✅ **File Output Support**: `/output` parameter for saving results to files
- ✅ **Error Handling**: Graceful error handling and user feedback
- ✅ **Color Support**: Consistent color scheme matching banner design
- ✅ **Professional Banner**: Subdued styling with disclaimers and credential checking

## Architecture

### Entry Point Logic
```bash
equasis                          # Auto-starts interactive mode
equasis --interactive            # Explicit interactive mode
equasis vessel --imo 1234567     # Traditional CLI mode
```

### Interactive Commands
```bash
> vessel /imo 1234567                        # Get comprehensive vessel data
> vessel /imo 1234567 /output vessel.json    # Save to file
> search /name "MAERSK"                      # Search vessels by name
> search /name "MAERSK" /output results.csv  # Save search results
> fleet /company "MSC"                       # Get fleet information
> format json                                # Set default output format
> status                                     # Show session status
> clear                                      # Clear screen
> help [command]                             # Show help
> help output                                # Show file output help
> exit                                       # Exit session
```

## Technical Implementation

### Core Files
- `equasis_cli/interactive.py` - Main interactive shell class
- `equasis_cli/main.py` - Dual-mode entry point detection
- `equasis_cli/__init__.py` - Package exports

### Key Classes and Methods

#### InteractiveShell Class
```python
class InteractiveShell(cmd.Cmd):
    def __init__(self):
        self.client = None              # Lazy authentication
        self.formatter = OutputFormatter()
        self.output_format = 'table'
        self.logged_in = False

    def parse_slash_command(self, line, expected_params):
        # Parse /param value syntax

    def ensure_authenticated(self):
        # Handle authentication and reconnection

    def do_vessel(self, line):
        # vessel /imo 1234567 [/format json]

    def do_search(self, line):
        # search /name "vessel name" [/format json]

    def do_fleet(self, line):
        # fleet /company "company name" [/format json]
```

### Session Management
- **Lazy Authentication**: Only authenticate when first command is run
- **Connection Persistence**: Keep Equasis session alive between commands
- **Auto-Reconnection**: Automatically handle session expiration
- **Credential Detection**: Show setup note if credentials missing

### Command Parsing
- **Regex-Based Parsing**: `/(\w+)\s+(?:"([^"]+)"|(\S+))`
- **Quoted Value Support**: `/name "vessel with spaces"`
- **Parameter Validation**: Check required vs optional parameters
- **Format Validation**: Validate output format options

## User Experience Features

### Startup Experience
1. **Auto-Detection**: `equasis` with no args starts interactive mode
2. **Banner Display**: Shows full banner with disclaimers on startup
3. **Credential Check**: Shows setup note if credentials not configured
4. **Connection Status**: Shows connection progress when first authenticated

### Interactive Commands
1. **Slash Syntax**: Modern `/param value` syntax like Claude Code
2. **Flexible Quoting**: Support both `"quoted values"` and `unquoted`
3. **Format Control**: Per-command format override or global default
4. **Error Recovery**: Commands fail gracefully without exiting session

### Help System
1. **General Help**: `help` shows all available commands
2. **Command Help**: `help vessel` shows command-specific usage
3. **Interactive Examples**: Real examples with actual data
4. **Parameter Reference**: Clear parameter documentation

### Session Management
1. **Status Command**: Shows connection status, format, debug mode
2. **Format Command**: Set global default output format
3. **Clear Command**: Clear screen for better readability
4. **Exit Handling**: Graceful exit with Ctrl+D, `exit`, or `quit`

## Benefits Achieved

### Performance Benefits
- **No Re-Authentication**: Session persists across commands
- **Faster Queries**: No startup overhead for subsequent commands
- **Connection Reuse**: Efficient use of Equasis connections

### User Experience Benefits
- **Modern Interface**: Slash commands feel contemporary
- **Exploration Friendly**: Easy to try multiple queries
- **Less Typing**: Shorter commands, no need for `--` flags
- **Visual Feedback**: Clear status and progress indicators

### Developer Benefits
- **Backward Compatibility**: Traditional CLI still works
- **Clean Architecture**: Separates interactive and traditional modes
- **Extensible**: Easy to add new commands and features

## Future Enhancements

### Phase 2 Features (Not Yet Implemented)
- **Command History**: Up/down arrow command history
- **Tab Completion**: Auto-complete commands and parameters
- **Multi-line Commands**: Support for complex queries
- **Result Variables**: Store and reuse query results
- **Session Export**: Export entire session to file

### Advanced Features (Future)
- **Batch Commands**: Run multiple commands from file
- **Watch Commands**: Continuously monitor vessel status
- **Comparison Tools**: Compare multiple vessels side-by-side
- **Data Pipeline**: Chain commands together

## Testing Strategy

### Manual Testing Completed
- ✅ Interactive mode startup
- ✅ All slash commands (vessel, search, fleet)
- ✅ Format switching and validation
- ✅ Authentication flow and reconnection
- ✅ Error handling and recovery
- ✅ Help system and documentation
- ✅ Exit handling (exit, quit, Ctrl+D)

### Integration Testing
- ✅ Traditional CLI mode still works
- ✅ Dual-mode detection logic
- ✅ Package imports and exports
- ✅ Color support across terminals

## Migration and Compatibility

### Backward Compatibility
- **100% Compatible**: All existing CLI commands work unchanged
- **No Breaking Changes**: Traditional usage patterns preserved
- **Optional Feature**: Interactive mode is additive, not replacement

### Migration Path
1. **Immediate**: Users can try interactive mode with `equasis`
2. **Gradual**: Users can switch between modes as needed
3. **Documentation**: README updated with both usage patterns

## Documentation Updates Needed

### README Updates
- Add interactive mode section
- Update quick start examples
- Document slash command syntax
- Add interactive vs traditional comparison

### Help Updates
- Update `--help` to mention interactive mode
- Add interactive mode examples
- Document session management features

## Summary

The interactive mode implementation successfully transforms Equasis CLI into a modern, user-friendly maritime intelligence tool. The implementation:

1. **Preserves Compatibility**: Traditional CLI still works perfectly
2. **Modern UX**: Slash commands and persistent sessions
3. **Professional Quality**: Consistent with existing banner and color design
4. **Extensible Architecture**: Easy to add future enhancements
5. **Robust Error Handling**: Graceful failure and recovery

The interactive mode makes maritime data exploration significantly more efficient and enjoyable, positioning Equasis CLI as a professional-grade maritime intelligence platform.