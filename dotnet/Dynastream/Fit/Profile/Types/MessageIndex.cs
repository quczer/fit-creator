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
    /// Implements the profile MessageIndex type as a class
    /// </summary>
    public static class MessageIndex 
    {
        public const ushort Selected = 0x8000; // message is selected if set
        public const ushort Reserved = 0x7000; // reserved (default 0)
        public const ushort Mask = 0x0FFF; // index
        public const ushort Invalid = (ushort)0xFFFF;


    }
}

