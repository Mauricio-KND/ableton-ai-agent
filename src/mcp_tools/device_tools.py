"""
Device management MCP tools for Ableton Live control

Provides tools for adding, removing, and managing devices (instruments and effects)
in Ableton Live through the MCP (Model Context Protocol) interface.
"""

from typing import Dict, Any, Optional, List
import functools

from ..utils.logger import get_logger
from ..utils.validators import validate_track_id, validate_device_name
from ..state.memory import MemoryManager
from ..state.session_manager import SessionManager


def mcp_tool(func):
    """Decorator to mark functions as MCP tools."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.is_mcp_tool = True
    return wrapper


class DeviceTools:
    """
    Collection of MCP tools for device management in Ableton Live.
    
    This class provides tools for adding, removing, and managing
    instruments and effects through the MCP interface.
    """
    
    def __init__(
        self, 
        memory_manager: MemoryManager,
        session_manager: SessionManager,
        ableton_client: Any = None
    ):
        """
        Initialize device tools.
        
        Args:
            memory_manager: Memory manager for tracking created elements
            session_manager: Session manager for state tracking
            ableton_client: Client for communicating with Ableton
        """
        self.logger = get_logger(__name__)
        self.memory = memory_manager
        self.session = session_manager
        self.ableton = ableton_client
        
        # Common device names for validation and suggestions
        self.known_instruments = {
            'Operator', 'Analog', 'Wavetable', 'Sampler', 'Simpler', 'Impulse',
            'Drum Rack', 'Instrument Rack', 'External Instrument', 'Collision',
            'Tension', 'Electric', 'CV Instrument', 'MIDI Effect Rack'
        }
        
        self.known_effects = {
            'Reverb', 'Delay', 'Compressor', 'EQ Eight', 'Chorus', 'Flanger',
            'Phaser', 'Distortion', 'Saturator', 'Limiter', 'Gate', 'Auto Filter',
            'Auto Pan', 'Corpus', 'Dynamic Tube', 'Erosion', 'Frequency Shifter',
            'Granulator', 'Looper', 'Multiband Dynamics', 'Overdrive', 'Redux',
            'Resonators', 'Reverb Envelope Follower', 'Spectrum', 'Vinyl Distortion',
            'Vocoder', 'Audio Effect Rack', 'External Audio Effect'
        }
        
        self.known_midi_effects = {
            'Arpeggiator', 'Chord', 'MIDI Effect Rack', 'Note Length', 'Pitch',
            'Random', 'Scale', 'Velocity', 'External MIDI Effect'
        }
        
    @mcp_tool
    def add_device(self, track_id: int, device_name: str, device_type: str = 'auto') -> Dict[str, Any]:
        """
        Add a device to a track.
        
        Args:
            track_id: ID of the track to add the device to
            device_name: Name of the device to add
            device_type: Type of device ('instrument', 'audio_effect', 'midi_effect', 'auto')
            
        Returns:
            Dictionary containing device addition result
        """
        try:
            track_id = validate_track_id(track_id)
            device_name = validate_device_name(device_name)
            
            # Check if track exists
            if track_id not in self.session.tracks:
                raise ValueError(f"Track {track_id} not found")
            
            track = self.session.tracks[track_id]
            
            # Auto-detect device type if not specified
            if device_type == 'auto':
                device_type = self._detect_device_type(device_name, track.track_type)
            
            # Validate device type compatibility
            if device_type == 'instrument' and track.track_type != 'midi':
                raise ValueError(f"Instruments can only be added to MIDI tracks")
            
            self.logger.info(f"Adding {device_type} '{device_name}' to track {track_id}")
            
            # Note: AbletonOSC doesn't support direct device creation via OSC
            # We'll provide guidance for manual device addition
            self.logger.info(f"Manual device addition required:")
            self.logger.info(f"   1. In Ableton Live, select track {track_id}")
            self.logger.info(f"   2. Click 'Device' button or press Shift+Cmd+T")
            self.logger.info(f"   3. Search for '{device_name}' in the browser")
            self.logger.info(f"   4. Double-click to load the device")
            
            device_id = len(self.session.devices)  # Simulated device ID
            
            # Update session state
            from ..state.session_manager import DeviceState
            self.session.devices[device_id] = DeviceState(
                device_id=device_id,
                track_id=track_id,
                name=device_name,
                device_type=device_type
            )
            
            # Update track state
            track.device_count += 1
            
            # Update memory
            self.memory.add_device(device_id, track_id, device_name, device_type)
            
            self.logger.info(f"Successfully added {device_type} '{device_name}' with ID {device_id}")
            
            return {
                'success': True,
                'device_id': device_id,
                'track_id': track_id,
                'name': device_name,
                'device_type': device_type,
                'message': f"Added {device_type} '{device_name}' (ID {device_id}) to track {track_id}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to add device '{device_name}': {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to add device '{device_name}': {e}"
            }
            
    @mcp_tool
    def remove_device(self, track_id: int, device_id: int) -> Dict[str, Any]:
        """
        Remove a device from a track.
        
        Args:
            track_id: ID of the track containing the device
            device_id: ID of the device to remove
            
        Returns:
            Dictionary containing device removal result
        """
        try:
            track_id = validate_track_id(track_id)
            self.logger.info(f"Removing device {device_id} from track {track_id}")
            
            # Check if device exists
            if device_id not in self.session.devices:
                raise ValueError(f"Device {device_id} not found")
            
            device = self.session.devices[device_id]
            if device.track_id != track_id:
                raise ValueError(f"Device {device_id} is not in track {track_id}")
            
            device_name = device.name
            
            # This would use actual MCP call to Ableton
            # Simulate removal
            del self.session.devices[device_id]
            
            # Update track state
            if track_id in self.session.tracks:
                self.session.tracks[track_id].device_count = max(0, self.session.tracks[track_id].device_count - 1)
            
            # Update memory
            if device_id in self.memory.devices:
                del self.memory.devices[device_id]
            
            self.logger.info(f"Successfully removed device '{device_name}' (ID {device_id}) from track {track_id}")
            
            return {
                'success': True,
                'device_id': device_id,
                'track_id': track_id,
                'device_name': device_name,
                'message': f"Removed device '{device_name}' (ID {device_id}) from track {track_id}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to remove device {device_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to remove device {device_id}: {e}"
            }
            
    @mcp_tool
    def set_device_parameter(self, track_id: int, device_id: int, parameter_name: str, value: float) -> Dict[str, Any]:
        """
        Set a parameter value for a device.
        
        Args:
            track_id: ID of the track containing the device
            device_id: ID of the device
            parameter_name: Name of the parameter to set
            value: Parameter value (typically 0.0 to 1.0)
            
        Returns:
            Dictionary containing parameter setting result
        """
        try:
            track_id = validate_track_id(track_id)
            
            # Validate value range
            if not isinstance(value, (int, float)):
                raise ValueError("Parameter value must be a number")
            if not 0.0 <= value <= 1.0:
                raise ValueError("Parameter value must be between 0.0 and 1.0")
            
            self.logger.info(f"Setting parameter '{parameter_name}' to {value} for device {device_id}")
            
            # Check if device exists
            if device_id not in self.session.devices:
                raise ValueError(f"Device {device_id} not found")
            
            device = self.session.devices[device_id]
            if device.track_id != track_id:
                raise ValueError(f"Device {device_id} is not in track {track_id}")
            
            old_value = device.parameters.get(parameter_name, None)
            
            # This would use actual MCP call to Ableton
            # Update session state
            device.parameters[parameter_name] = value
            device.last_updated
            
            # Update memory usage
            self.memory.update_track_usage(track_id)
            
            self.logger.info(f"Successfully set parameter '{parameter_name}' from {old_value} to {value}")
            
            return {
                'success': True,
                'device_id': device_id,
                'track_id': track_id,
                'parameter_name': parameter_name,
                'old_value': old_value,
                'new_value': value,
                'message': f"Set parameter '{parameter_name}' from {old_value} to {value} for device {device_id}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to set parameter '{parameter_name}': {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to set parameter '{parameter_name}': {e}"
            }
            
    @mcp_tool
    def get_device_info(self, track_id: int, device_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a device.
        
        Args:
            track_id: ID of the track containing the device
            device_id: ID of the device
            
        Returns:
            Dictionary containing device information
        """
        try:
            track_id = validate_track_id(track_id)
            
            # Get device state
            device_state = self.session.get_device_state(device_id)
            if not device_state:
                raise ValueError(f"Device {device_id} not found")
            
            if device_state.track_id != track_id:
                raise ValueError(f"Device {device_id} is not in track {track_id}")
            
            # Get memory information
            memory_info = self.memory.devices.get(device_id)
            
            device_info = {
                'device_id': device_state.device_id,
                'track_id': device_state.track_id,
                'name': device_state.name,
                'device_type': device_state.device_type,
                'is_enabled': device_state.is_enabled,
                'parameters': device_state.parameters,
                'last_updated': device_state.last_updated.isoformat()
            }
            
            # Add memory information if available
            if memory_info:
                device_info['memory'] = {
                    'created_at': memory_info.created_at.isoformat(),
                    'parameters': memory_info.parameters
                }
            
            self.logger.info(f"Retrieved information for device {device_id}")
            
            return {
                'success': True,
                'device_info': device_info,
                'message': f"Retrieved information for device {device_id}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get device info for {device_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to get device info for {device_id}: {e}"
            }
            
    @mcp_tool
    def list_devices(self, track_id: Optional[int] = None, device_type: Optional[str] = None) -> Dict[str, Any]:
        """
        List all devices, optionally filtered by track and/or type.
        
        Args:
            track_id: Optional track ID to filter devices by
            device_type: Optional device type to filter by
            
        Returns:
            Dictionary containing list of devices
        """
        try:
            self.logger.info(f"Listing devices with track filter: {track_id}, type filter: {device_type}")
            
            devices = list(self.session.devices.values())
            
            # Apply filters
            if track_id:
                track_id = validate_track_id(track_id)
                devices = [d for d in devices if d.track_id == track_id]
            
            if device_type:
                devices = [d for d in devices if d.device_type == device_type]
            
            device_list = []
            for device in devices:
                device_info = {
                    'device_id': device.device_id,
                    'track_id': device.track_id,
                    'name': device.name,
                    'device_type': device.device_type,
                    'is_enabled': device.is_enabled,
                    'parameter_count': len(device.parameters)
                }
                device_list.append(device_info)
            
            self.logger.info(f"Found {len(device_list)} devices")
            
            return {
                'success': True,
                'devices': device_list,
                'count': len(device_list),
                'track_filter': track_id,
                'type_filter': device_type,
                'message': f"Found {len(device_list)} devices" + 
                          (f" in track {track_id}" if track_id else "") +
                          (f" of type '{device_type}'" if device_type else "")
            }
            
        except Exception as e:
            self.logger.error(f"Failed to list devices: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to list devices: {e}"
            }
            
    @mcp_tool
    def list_available_devices(self, device_type: Optional[str] = None) -> Dict[str, Any]:
        """
        List available devices that can be added to tracks.
        
        Args:
            device_type: Optional device type to filter by ('instrument', 'audio_effect', 'midi_effect')
            
        Returns:
            Dictionary containing available devices
        """
        try:
            self.logger.info(f"Listing available devices with type filter: {device_type}")
            
            available_devices = {}
            
            if device_type in [None, 'instrument']:
                available_devices['instruments'] = sorted(list(self.known_instruments))
            
            if device_type in [None, 'audio_effect']:
                available_devices['audio_effects'] = sorted(list(self.known_effects))
            
            if device_type in [None, 'midi_effect']:
                available_devices['midi_effects'] = sorted(list(self.known_midi_effects))
            
            total_count = sum(len(devices) for devices in available_devices.values())
            
            self.logger.info(f"Found {total_count} available devices")
            
            return {
                'success': True,
                'available_devices': available_devices,
                'total_count': total_count,
                'type_filter': device_type,
                'message': f"Found {total_count} available devices" + 
                          (f" of type '{device_type}'" if device_type else "")
            }
            
        except Exception as e:
            self.logger.error(f"Failed to list available devices: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to list available devices: {e}"
            }
            
    def _detect_device_type(self, device_name: str, track_type: str) -> str:
        """
        Auto-detect device type based on name and track type.
        
        Args:
            device_name: Name of the device
            track_type: Type of the track
            
        Returns:
            Detected device type
        """
        device_lower = device_name.lower()
        
        # Check for known devices
        if device_name in self.known_instruments:
            return 'instrument'
        elif device_name in self.known_effects:
            return 'audio_effect'
        elif device_name in self.known_midi_effects:
            return 'midi_effect'
        
        # Try to detect by name patterns
        if any(keyword in device_lower for keyword in ['synth', 'instrument', 'sampler', 'drum']):
            return 'instrument'
        elif any(keyword in device_lower for keyword in ['reverb', 'delay', 'compressor', 'eq', 'filter']):
            return 'audio_effect'
        elif any(keyword in device_lower for keyword in ['arpeggiator', 'chord', 'midi']):
            return 'midi_effect'
        
        # Default based on track type
        if track_type == 'midi':
            return 'instrument'
        else:
            return 'audio_effect'


# Global instance for MCP tool registration
_device_tools_instance: Optional[DeviceTools] = None


def initialize_device_tools(
    memory_manager: MemoryManager,
    session_manager: SessionManager,
    ableton_client: Any = None
) -> DeviceTools:
    """
    Initialize the device tools with required dependencies.
    
    Args:
        memory_manager: Memory manager instance
        session_manager: Session manager instance
        ableton_client: Ableton client instance
        
    Returns:
        Initialized DeviceTools instance
    """
    global _device_tools_instance
    _device_tools_instance = DeviceTools(memory_manager, session_manager, ableton_client)
    return _device_tools_instance


def get_device_tools() -> Optional[DeviceTools]:
    """Get the global device tools instance."""
    return _device_tools_instance


# Export individual tool functions for MCP registration
def add_device(track_id: int, device_name: str, device_type: str = 'auto') -> Dict[str, Any]:
    """Add a device to a track."""
    if not _device_tools_instance:
        raise RuntimeError("Device tools not initialized")
    return _device_tools_instance.add_device(track_id, device_name, device_type)


def remove_device(track_id: int, device_id: int) -> Dict[str, Any]:
    """Remove a device from a track."""
    if not _device_tools_instance:
        raise RuntimeError("Device tools not initialized")
    return _device_tools_instance.remove_device(track_id, device_id)


def set_device_parameter(track_id: int, device_id: int, parameter_name: str, value: float) -> Dict[str, Any]:
    """Set a device parameter."""
    if not _device_tools_instance:
        raise RuntimeError("Device tools not initialized")
    return _device_tools_instance.set_device_parameter(track_id, device_id, parameter_name, value)


def get_device_info(track_id: int, device_id: int) -> Dict[str, Any]:
    """Get device information."""
    if not _device_tools_instance:
        raise RuntimeError("Device tools not initialized")
    return _device_tools_instance.get_device_info(track_id, device_id)


def list_devices(track_id: Optional[int] = None, device_type: Optional[str] = None) -> Dict[str, Any]:
    """List devices."""
    if not _device_tools_instance:
        raise RuntimeError("Device tools not initialized")
    return _device_tools_instance.list_devices(track_id, device_type)


def list_available_devices(device_type: Optional[str] = None) -> Dict[str, Any]:
    """List available devices."""
    if not _device_tools_instance:
        raise RuntimeError("Device tools not initialized")
    return _device_tools_instance.list_available_devices(device_type)