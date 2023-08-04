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
    /// Implements the profile LeftRightBalance100 type as a class
    /// </summary>
    public static class LeftRightBalance100 
    {
        public const ushort Mask = 0x3FFF; // % contribution scaled by 100
        public const ushort Right = 0x8000; // data corresponds to right if set, otherwise unknown
        public const ushort Invalid = (ushort)0xFFFF;


    }
}

