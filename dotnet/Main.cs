using WourkoutSerialization;
using Dynastream.Fit;
namespace main
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length < 2)
            {
                Console.WriteLine("Usage: dotnet run <json_wourkout_path> <fit_wourkout_path>");
                // CreateBikeTempoWorkout(new FileStream(args[0], FileMode.Create));
                return;
            }
            var messages = JSONDeserializer.DeserializeWorkout(args[0]);
            Console.WriteLine($"Deserialized {messages.Count} messages from {args[0]}");
            FITSerializer.SerializeWorkout(messages, new FileStream(args[1], FileMode.Create));
            Console.WriteLine($"Saved serialized {messages.Count} messages in {args[1]}");

        }
        static void CreateBikeTempoWorkout(FileStream file)
        {
            var workoutSteps = new List<WorkoutStepMesg>();

            workoutSteps.Add(CreateWorkoutStep(messageIndex: workoutSteps.Count,
                                       durationType: WktStepDuration.Time,
                                       durationValue: 600000, // milliseconds
                                       targetType: WktStepTarget.HeartRate,
                                       targetValue: 1,
                                       intensity: Intensity.Warmup));

            workoutSteps.Add(CreateWorkoutStep(messageIndex: workoutSteps.Count,
                                                durationType: WktStepDuration.Time,
                                                durationValue: 2400000, // milliseconds
                                                targetType: WktStepTarget.Power,
                                                customTargetValueLow: 34,
                                                customTargetValueHigh: 50));

            workoutSteps.Add(CreateWorkoutStep(messageIndex: workoutSteps.Count,
                                                intensity: Intensity.Cooldown));

            var workoutMesg = new WorkoutMesg();
            workoutMesg.SetWktName("garmin_tempo_bike_workout");
            workoutMesg.SetSport(Sport.Cycling);
            workoutMesg.SetSubSport(SubSport.Invalid);
            workoutMesg.SetNumValidSteps((ushort)workoutSteps.Count);

            CreateWorkout(workoutMesg, workoutSteps, file);
        }

        static void CreateWorkout(WorkoutMesg workoutMesg, List<WorkoutStepMesg> workoutSteps, FileStream file)
        {
            // The combination of file type, manufacturer id, product id, and serial number should be unique.
            // When available, a non-random serial number should be used.
            Dynastream.Fit.File fileType = Dynastream.Fit.File.Workout;
            ushort manufacturerId = Manufacturer.Development;
            ushort productId = 0;
            Random random = new Random();
            uint serialNumber = (uint)random.Next();

            // Every FIT file MUST contain a File ID message
            var fileIdMesg = new FileIdMesg();
            fileIdMesg.SetType(fileType);
            fileIdMesg.SetManufacturer(manufacturerId);
            fileIdMesg.SetProduct(productId);
            fileIdMesg.SetTimeCreated(new Dynastream.Fit.DateTime(System.DateTime.UtcNow));
            fileIdMesg.SetSerialNumber(serialNumber);

            // Create the output stream, this can be any type of stream, including a file or memory stream. Must have read/write access

            // Create a FIT Encode object
            Encode encoder = new Encode(ProtocolVersion.V10);

            // Write the FIT header to the output stream
            encoder.Open(file);

            // Write the messages to the file, in the proper sequence
            encoder.Write(fileIdMesg);
            encoder.Write(workoutMesg);

            foreach (WorkoutStepMesg workoutStep in workoutSteps)
            {
                encoder.Write(workoutStep);
            }

            // Update the data size in the header and calculate the CRC
            encoder.Close();

            // Close the output stream
            file.Close();

            Console.WriteLine($"Encoded FIT file {file.Name}");
        }

        private static WorkoutStepMesg CreateWorkoutStep(int messageIndex, String name = null, String notes = null, Intensity intensity = Intensity.Active, WktStepDuration durationType = WktStepDuration.Open, uint? durationValue = null, WktStepTarget targetType = WktStepTarget.Open, uint targetValue = 0, uint? customTargetValueLow = null, uint? customTargetValueHigh = null)
        {
            if (durationType == WktStepDuration.Invalid)
            {
                return null;
            }

            var workoutStepMesg = new WorkoutStepMesg();
            workoutStepMesg.SetMessageIndex((ushort)messageIndex);

            if (name != null)
            {
                workoutStepMesg.SetWktStepName(name);
            }

            if (notes != null)
            {
                workoutStepMesg.SetNotes(notes);
            }

            workoutStepMesg.SetIntensity(intensity);
            workoutStepMesg.SetDurationType(durationType);

            if (durationValue.HasValue)
            {
                workoutStepMesg.SetDurationValue(durationValue);
            }

            if (targetType != WktStepTarget.Invalid && customTargetValueLow.HasValue && customTargetValueHigh.HasValue)
            {
                workoutStepMesg.SetTargetType(targetType);
                workoutStepMesg.SetTargetValue(0);
                workoutStepMesg.SetCustomTargetValueLow(customTargetValueLow);
                workoutStepMesg.SetCustomTargetValueHigh(customTargetValueHigh);
            }
            else if (targetType != WktStepTarget.Invalid)
            {
                workoutStepMesg.SetTargetType(targetType);
                workoutStepMesg.SetTargetValue(targetValue);
                workoutStepMesg.SetCustomTargetValueLow(0);
                workoutStepMesg.SetCustomTargetValueHigh(0);
            }

            return workoutStepMesg;
        }
    }
}