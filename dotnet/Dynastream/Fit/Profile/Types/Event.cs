#region Copyright
/////////////////////////////////////////////////////////////////////////////////////////////
// Copyright 2023 Garmin International, Inc.
// Licensed under the Flexible and Interoperable Data Transfer (FIT) Protocol License; you
// may not use this file except in compliance with the Flexible and Interoperable Data
// Transfer (FIT) Protocol License.
/////////////////////////////////////////////////////////////////////////////////////////////
// ****WARNING****  This file is auto-generated!  Do NOT edit this file.
// Profile Version = 21.115Release
// Tag = production/release/21.115.00-0-gfe0a7f8
/////////////////////////////////////////////////////////////////////////////////////////////

#endregion

namespace Dynastream.Fit
{
    /// <summary>
    /// Implements the profile Event type as an enum
    /// </summary>
    public enum Event : byte
    {
        Timer = 0,
        Workout = 3,
        WorkoutStep = 4,
        PowerDown = 5,
        PowerUp = 6,
        OffCourse = 7,
        Session = 8,
        Lap = 9,
        CoursePoint = 10,
        Battery = 11,
        VirtualPartnerPace = 12,
        HrHighAlert = 13,
        HrLowAlert = 14,
        SpeedHighAlert = 15,
        SpeedLowAlert = 16,
        CadHighAlert = 17,
        CadLowAlert = 18,
        PowerHighAlert = 19,
        PowerLowAlert = 20,
        RecoveryHr = 21,
        BatteryLow = 22,
        TimeDurationAlert = 23,
        DistanceDurationAlert = 24,
        CalorieDurationAlert = 25,
        Activity = 26,
        FitnessEquipment = 27,
        Length = 28,
        UserMarker = 32,
        SportPoint = 33,
        Calibration = 36,
        FrontGearChange = 42,
        RearGearChange = 43,
        RiderPositionChange = 44,
        ElevHighAlert = 45,
        ElevLowAlert = 46,
        CommTimeout = 47,
        AutoActivityDetect = 54,
        DiveAlert = 56,
        DiveGasSwitched = 57,
        TankPressureReserve = 71,
        TankPressureCritical = 72,
        TankLost = 73,
        RadarThreatAlert = 75,
        TankBatteryLow = 76,
        TankPodConnected = 81,
        TankPodDisconnected = 82,
        Invalid = 0xFF


    }
}

