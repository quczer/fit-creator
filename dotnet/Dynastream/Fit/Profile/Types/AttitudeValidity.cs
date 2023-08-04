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
    /// Implements the profile AttitudeValidity type as a class
    /// </summary>
    public static class AttitudeValidity 
    {
        public const ushort TrackAngleHeadingValid = 0x0001;
        public const ushort PitchValid = 0x0002;
        public const ushort RollValid = 0x0004;
        public const ushort LateralBodyAccelValid = 0x0008;
        public const ushort NormalBodyAccelValid = 0x0010;
        public const ushort TurnRateValid = 0x0020;
        public const ushort HwFail = 0x0040;
        public const ushort MagInvalid = 0x0080;
        public const ushort NoGps = 0x0100;
        public const ushort GpsInvalid = 0x0200;
        public const ushort SolutionCoasting = 0x0400;
        public const ushort TrueTrackAngle = 0x0800;
        public const ushort MagneticHeading = 0x1000;
        public const ushort Invalid = (ushort)0xFFFF;


    }
}

