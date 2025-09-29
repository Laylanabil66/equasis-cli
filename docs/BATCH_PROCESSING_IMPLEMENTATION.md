# Batch Processing Implementation Plan for equasis-cli

## Executive Summary

This document outlines the implementation of batch processing functionality for equasis-cli, enabling users to efficiently query multiple vessel IMO numbers in a single operation. The feature will be available in both interactive and traditional CLI modes, with comprehensive error handling, progress tracking, and multiple output format support.

## Current State Analysis

### Existing Architecture
- **Single vessel processing**: Currently processes one IMO at a time
- **Session persistence**: Authentication session maintained across requests (especially in interactive mode)
- **Rate limiting**: Built-in 1-second delay between API requests
- **Output formats**: Supports table, JSON, and CSV formats
- **Modular design**: Clear separation between client, parser, and formatter components

### Limitations
- No support for multiple IMO processing in single command
- No batch file input capability
- No progress indicators for multiple operations
- No batch-specific error handling or reporting

## Implementation Design

### 1. Data Structures

#### BatchResult Class
```python
@dataclass
class BatchResult:
    imo: str
    success: bool
    vessel_data: Optional[EquasisVesselData]
    error_message: Optional[str]
    processing_time: float
```

#### BatchSummary Class
```python
@dataclass
class BatchSummary:
    total_vessels: int
    successful: int
    failed: int
    processing_time: float
    failed_imos: List[str]
```

### 2. Interactive Mode Enhancement

#### New Command: `batch`
```
Syntax:
  batch /imos "IMO1,IMO2,IMO3" [/format FORMAT] [/output FILE]
  batch /file FILENAME [/format FORMAT] [/output FILE]

Examples:
  batch /imos "9074729,8515128,9632179"
  batch /file fleet_imos.txt /format json /output results.json
  batch /imos "9074729,8515128" /progress
```

#### Implementation in interactive.py
```python
def do_batch(self, line: str):
    """Process multiple vessels in batch"""
    # Parse parameters
    # Handle both /imos and /file input
    # Show progress indicator
    # Collect results
    # Format and output
```

### 3. Traditional CLI Mode Enhancement

#### Modified vessel command
```bash
# Multiple IMOs directly
equasis vessel --imo 9074729 8515128 9632179

# IMOs from file
equasis vessel --imo-file fleet_imos.txt

# With output options
equasis vessel --imo 9074729 8515128 --output json --output-file results.json

# With error handling options
equasis vessel --imo-file large_fleet.txt --continue-on-error --progress
```

### 4. Client Module Extensions

#### New Method: search_vessels_by_imo_batch
```python
def search_vessels_by_imo_batch(
    self,
    imos: List[str],
    progress_callback: Optional[Callable] = None,
    stop_on_error: bool = False
) -> List[BatchResult]:
    """
    Process multiple IMO numbers with progress tracking

    Args:
        imos: List of IMO numbers to process
        progress_callback: Optional callback for progress updates
        stop_on_error: Whether to stop processing on first error

    Returns:
        List of BatchResult objects
    """
```

### 5. Formatter Module Extensions

#### Batch JSON Format
```json
{
  "batch_summary": {
    "total_vessels": 3,
    "successful": 2,
    "failed": 1,
    "processing_time": 4.5,
    "timestamp": "2025-09-29T14:30:00Z"
  },
  "results": [
    {
      "imo": "9074729",
      "success": true,
      "vessel_data": { ... }
    },
    {
      "imo": "8515128",
      "success": false,
      "error": "Vessel not found"
    }
  ]
}
```

#### Batch CSV Format
```csv
IMO,Name,Flag,Type,GT,DWT,Year,Status,Error
9074729,EMMA MAERSK,Denmark,Container,170794,156907,2006,Active,
8515128,,,,,,,,"Vessel not found"
```

#### Batch Table Format
```
Batch Processing Results
========================
Total Vessels: 3
Successful: 2
Failed: 1
Processing Time: 4.5s

Successfully Retrieved:
-----------------------
IMO       | Name          | Flag     | Type      | GT      | Year
9074729   | EMMA MAERSK   | Denmark  | Container | 170,794 | 2006
9632179   | MSC OSCAR     | Panama   | Container | 192,237 | 2014

Failed Lookups:
---------------
IMO       | Error
8515128   | Vessel not found
```

### 6. Progress Indicators

#### Interactive Mode
```
Processing vessels: [████████████████████████░░░░░░] 12/15 (80%)
Current: IMO 9074729 - EMMA MAERSK
```

#### Traditional CLI Mode
```
[1/15] Processing IMO 9074729... ✓
[2/15] Processing IMO 8515128... ✗ (Not found)
[3/15] Processing IMO 9632179... ✓
```

### 7. Error Handling Strategy

#### Error Types
1. **Network errors**: Retry with exponential backoff
2. **Authentication errors**: Re-authenticate once, then fail
3. **Vessel not found**: Record and continue
4. **Rate limiting**: Respect delays, adjust timing
5. **Invalid IMO format**: Skip with warning

#### Error Recovery
- Automatic retry for transient failures (max 3 attempts)
- Session refresh on authentication timeout
- Detailed error logging for troubleshooting
- Summary report of all failures at end

### 8. File Input Formats

#### Supported Formats
- **Plain text**: One IMO per line
- **CSV**: IMO in first column, other columns ignored
- **JSON**: Array of IMO strings or objects with 'imo' field

#### Example: fleet_imos.txt
```
9074729
8515128
9632179
# Comments supported
9839333
```

## Implementation Phases

### Phase 1: Core Batch Processing (Week 1)
- [ ] Create BatchResult and BatchSummary dataclasses
- [ ] Implement search_vessels_by_imo_batch in client
- [ ] Basic progress callback mechanism
- [ ] Simple error collection

### Phase 2: Interactive Mode (Week 1)
- [ ] Add do_batch command
- [ ] Implement /imos parameter parsing
- [ ] Implement /file parameter with file reading
- [ ] Add progress display
- [ ] Integrate with existing output handling

### Phase 3: Traditional CLI Mode (Week 2)
- [ ] Modify argument parser for multiple IMOs
- [ ] Add --imo-file option
- [ ] Implement batch processing logic
- [ ] Add --continue-on-error flag
- [ ] Add --progress flag

### Phase 4: Formatter Updates (Week 2)
- [ ] Implement format_batch_vessel_info
- [ ] JSON array formatting
- [ ] CSV batch formatting
- [ ] Table summary formatting
- [ ] Error report formatting

### Phase 5: Testing & Documentation (Week 3)
- [ ] Unit tests for batch processing
- [ ] Integration tests with real API
- [ ] Performance testing with large batches
- [ ] Update README with examples
- [ ] Update help text in both modes

## Performance Considerations

### Rate Limiting
- Maintain 1-second minimum between requests
- Implement adaptive rate limiting based on server responses
- Consider parallel processing with controlled concurrency (future)

### Memory Management
- Stream results to file for large batches
- Implement result pagination for display
- Clear processed results from memory after writing

### Session Management
- Keep session alive during long batch operations
- Implement session refresh mechanism
- Handle session timeout gracefully

## Testing Strategy

### Test Cases
1. **Small batch (3-5 vessels)**: Basic functionality
2. **Medium batch (10-20 vessels)**: Progress tracking
3. **Large batch (50+ vessels)**: Performance and memory
4. **Mixed valid/invalid IMOs**: Error handling
5. **File input variations**: Different formats
6. **Network interruptions**: Recovery mechanisms
7. **Authentication timeout**: Session refresh

### Test Data
```python
TEST_IMOS = [
    "9074729",  # Valid - EMMA MAERSK
    "8515128",  # Invalid - Not found
    "9632179",  # Valid - MSC OSCAR
    "invalid",  # Invalid format
    "9839333",  # Valid - EVER GIVEN
]
```

## Success Metrics

### Functional Requirements
- ✓ Process 10+ vessels without timeout
- ✓ Maintain rate limiting compliance
- ✓ Generate valid output in all formats
- ✓ Provide real-time progress feedback
- ✓ Handle errors without stopping batch
- ✓ Support file input in multiple formats

### Performance Requirements
- Process 50 vessels in < 60 seconds
- Memory usage < 100MB for 100 vessels
- Error recovery success rate > 90%
- Zero data loss on interruption

### User Experience
- Clear progress indicators
- Informative error messages
- Intuitive command syntax
- Comprehensive help documentation
- Consistent behavior across modes

## Migration Path

### Backward Compatibility
- Existing single-vessel commands unchanged
- New batch functionality is additive
- No breaking changes to API or output formats

### User Communication
1. Update README with prominent batch processing section
2. Add examples to help text
3. Create migration guide for power users
4. Announce in release notes

## Future Enhancements

### Version 2.0
- Parallel processing with worker threads
- Resume interrupted batch operations
- Batch query optimization
- Export to Excel format
- Email notification on completion

### Version 3.0
- Scheduled batch processing
- Differential updates (only changed data)
- Integration with vessel tracking services
- Webhook notifications
- REST API endpoint for batch operations

## Conclusion

This batch processing implementation will significantly enhance equasis-cli's capability to handle fleet-scale vessel queries efficiently. The phased approach ensures stable delivery while maintaining backward compatibility and providing clear value to users from the first release.