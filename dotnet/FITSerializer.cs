using Dynastream.Fit;

namespace WourkoutSerialization
{
    class FITSerializer
    {
        public static void SerializeWorkout(List<Mesg> messages, FileStream destination)
        {
            Encode encoder = new Encode(ProtocolVersion.V10);
            encoder.Open(destination);

            foreach (var message in messages)
            {
                encoder.Write(message);
            }

            // Update the data size in the header and calculate the CRC
            encoder.Close();

            // Close the output stream
            destination.Close();
        }

        public static void DeserializeWorkout(FileStream file)
        {
            Decode decoder = new Decode();
            Console.WriteLine($"is FIT = {decoder.IsFIT(file)}");
            Console.WriteLine($"is integral = {decoder.CheckIntegrity(file)}");
            Console.WriteLine($"is readable = {decoder.Read(file)}");
            decoder.Read(file);

            // foreach (var message in messages)
            // {
            //     encoder.Write(message);
            // }

            // // Update the data size in the header and calculate the CRC
            // encoder.Close();

            // // Close the output stream
            // destination.Close();
        }

    }
}