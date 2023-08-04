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

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.IO;

namespace Dynastream.Utility
{
    /// <summary>
    /// Extend framework BinaryWriter to support BigEndian destinations.
    /// When writing multibyte values, the bytes are reordered appropriately.
    /// </summary>
    public class EndianBinaryWriter : BinaryWriter
    {
        #region Fields
        private bool isBigEndian = false;
        #endregion

        #region Properties
        public bool IsBigEndian
        {
            get { return isBigEndian; }
            set { isBigEndian = value; }
        }
        #endregion

        #region Constructors
        public EndianBinaryWriter(Stream output, Encoding encoding, bool isBigEndian)
            : base(output, encoding)
        {
            this.isBigEndian = isBigEndian;
        }

        public EndianBinaryWriter(Stream output, bool isBigEndian)
            : this(output, Encoding.UTF8, isBigEndian)
        {
        }
        #endregion

        #region Methods
        public override void Write(short value)
        {
            if (!IsBigEndian)
            {
                base.Write(value);
                return;
            }
            byte[] buffer = BitConverter.GetBytes(value);
            Array.Reverse(buffer);
            base.Write(buffer, 0, 2);
        }

        public override void Write(ushort value)
        {
            if (!IsBigEndian)
            {
                base.Write(value);
                return;
            }
            byte[] buffer = BitConverter.GetBytes(value);
            Array.Reverse(buffer);
            base.Write(buffer, 0, 2);
        }

        public override void Write(int value)
        {
            if (!IsBigEndian)
            {
                base.Write(value);
                return;
            }
            byte[] buffer = BitConverter.GetBytes(value);
            Array.Reverse(buffer);
            base.Write(buffer, 0, 4);
        }

        public override void Write(uint value)
        {
            if (!IsBigEndian)
            {
                base.Write(value);
                return;
            }
            byte[] buffer = BitConverter.GetBytes(value);
            Array.Reverse(buffer);
            base.Write(buffer, 0, 4);
        }

        public override void Write(long value)
        {
            if (!IsBigEndian)
            {
                base.Write(value);
                return;
            }
            byte[] buffer = BitConverter.GetBytes(value);
            Array.Reverse(buffer);
            base.Write(buffer, 0, 8);
        }

        public override void Write(ulong value)
        {
            if (!IsBigEndian)
            {
                base.Write(value);
                return;
            }
            byte[] buffer = BitConverter.GetBytes(value);
            Array.Reverse(buffer);
            base.Write(buffer, 0, 8);
        }

        public override void Write(float value)
        {
            if (!IsBigEndian)
            {
                base.Write(value);
                return;
            }
            byte[] buffer = BitConverter.GetBytes(value);
            Array.Reverse(buffer);
            base.Write(buffer, 0, 4);
        }

        public override void Write(double value)
        {
            if (!IsBigEndian)
            {
                base.Write(value);
                return;
            }
            byte[] buffer = BitConverter.GetBytes(value);
            Array.Reverse(buffer);
            base.Write(buffer, 0, 8);
        }
        #endregion
    }
} // namespace
