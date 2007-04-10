#!/usr/bin/python

import dbus
import dbus.service
import dbus.glib
import gobject

bus = dbus.Bus (dbus.Bus.TYPE_SYSTEM)
hal_service = bus.get_service ('org.freedesktop.Hal')
hal_manager = hal_service.get_object ('/org/freedesktop/Hal/Manager','org.freedesktop.Hal.Manager')

volume_udi_list = hal_manager.FindDeviceByCapability ('volume')
for udi in volume_udi_list:
    volume = hal_service.get_object (udi, 'org.freedesktop.Hal.Device')
    device_file = volume.GetProperty ('block.device')
    fstype = volume.GetProperty ('volume.fstype')
    storage_udi = volume.GetProperty ('block.storage_device')
    storage = hal_service.get_object (storage_udi, 'org.freedesktop.Hal.Device')
    drive_type = storage.GetProperty ('storage.drive_type')
    print 'udi=%s device_file=%s fstype=%s drive_type=%s'%(udi, device_file, fstype, drive_type)
