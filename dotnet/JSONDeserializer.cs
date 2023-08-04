using Dynastream.Fit;
using System.Text.Json;

namespace WourkoutSerialization
{
    class JSONDeserializer
    {
        /// <summary>
        /// Deserializes only first `file_id_mesgs`, first `workout_mesgs` and all `workout_step_mesgs`.
        /// Assumes all timestamps to be in epoch format.
        /// </summary>

        public static List<Mesg> DeserializeWorkout(string fileAPath)
        {
            var json = System.IO.File.ReadAllText(fileAPath);
            JsonDocument wourkoutJson = JsonSerializer.Deserialize<JsonDocument>(json) ?? throw new Exception("Could not deserialize json");
            JsonElement wourkoutRoot = wourkoutJson.RootElement;

            var messages = new List<Mesg>
            {
                ExtractFileIdMesg(wourkoutRoot),
                ExtractWorkoutMesg(wourkoutRoot)
            };
            messages.AddRange(ExtractworkoutStepMesgs(wourkoutRoot));
            return messages;
        }

        /// <summary>
        /// Assumes the type of the workout to be `Manufacturer.Development`.
        /// </summary>
        static FileIdMesg ExtractFileIdMesg(JsonElement wourkoutRoot)
        {
            JsonElement json = wourkoutRoot.GetProperty("file_id_mesgs")[0];

            var msg = new FileIdMesg();
            msg.SetType(PropertyToEnum<Dynastream.Fit.File>(json.GetProperty("type").GetString()));
            msg.SetManufacturer(Manufacturer.Development);
            msg.SetProduct(json.GetProperty("product").GetUInt16());
            msg.SetTimeCreated(new Dynastream.Fit.DateTime(DateTimeOffset.FromUnixTimeSeconds(json.GetProperty("time_created").GetInt64()).DateTime));
            msg.SetSerialNumber(json.GetProperty("serial_number").GetUInt32());

            return msg;
        }

        static T PropertyToEnum<T>(string snakeCaseValue) where T : Enum
        {
            return (T)Enum.Parse(typeof(T), SnakeToCamelCase(snakeCaseValue));
        }

        static string SnakeToCamelCase(string snakeCaseValue)
        {
            return snakeCaseValue.Split(new[] { "_" }, StringSplitOptions.RemoveEmptyEntries).Select(s => char.ToUpperInvariant(s[0]) + s.Substring(1, s.Length - 1)).Aggregate(string.Empty, (s1, s2) => s1 + s2);

        }

        /// <summary>
        /// </summary>
        static WorkoutMesg ExtractWorkoutMesg(JsonElement wourkoutRoot)
        {
            JsonElement json = wourkoutRoot.GetProperty("workout_mesgs")[0];

            var msg = new WorkoutMesg();
            msg.SetWktName(json.GetProperty("wkt_name").GetString());
            msg.SetSport(PropertyToEnum<Dynastream.Fit.Sport>(json.GetProperty("sport").GetString()));
            msg.SetSubSport(PropertyToEnum<SubSport>(GetOptionalProperty<string>(json, "sub_sport", "invalid")));
            msg.SetNumValidSteps(json.GetProperty("num_valid_steps").GetUInt16());

            return msg;
        }

        // TODO: FIX
        static T? GetOptionalProperty<T>(JsonElement json, string propertyName, T? defaultValue = default)
        {
            Func<JsonElement, T> converter;
            if (typeof(T) == typeof(int))
            {
                converter = (JsonElement e) => (T)(object)e.GetInt32();
            }
            else if (typeof(T) == typeof(uint))
            {
                converter = (JsonElement e) => (T)(object)e.GetUInt32();
            }
            else if (typeof(T) == typeof(string))
            {
                converter = (JsonElement e) => (T)(object)e.GetString();
            }
            else
            {
                throw new Exception($"Unsupported type {typeof(T)}");
            }
            return json.TryGetProperty(propertyName, out JsonElement _) ? converter(json.GetProperty(propertyName)) : defaultValue;
        }
        static List<WorkoutStepMesg> ExtractworkoutStepMesgs(JsonElement wourkoutRoot)
        {
            JsonElement workoutArrayJson = wourkoutRoot.GetProperty("workout_step_mesgs");
            var messages = new List<WorkoutStepMesg>();

            for (int i = 0; i < workoutArrayJson.GetArrayLength(); i++)
            {
                JsonElement json = workoutArrayJson[i];
                var message = CreateWorkoutStep(
                    messageIndex: json.GetProperty("message_index").GetInt32(),
                    intensity: GetOptionalProperty<string>(json, "intensity"),
                    durationType: GetOptionalProperty<string>(json, "duration_type"),
                    durationValue: GetOptionalProperty<uint>(json, "duration_value"),
                    targetType: GetOptionalProperty<string>(json, "target_type"),
                    targetValue: GetOptionalProperty<uint>(json, "target_value"),
                    customTargetValueLow: GetOptionalProperty<uint>(json, "custom_target_value_low"),
                    customTargetValueHigh: GetOptionalProperty<uint>(json, "custom_target_value_high"),
                    secondaryTargetType: GetOptionalProperty<string>(json, "secondary_target_type"),
                    secondaryTargetValue: GetOptionalProperty<uint>(json, "secondary_target_value"),
                    secondaryCustomTargetValueLow: GetOptionalProperty<uint>(json, "secondary_custom_target_value_low"),
                    secondaryCustomTargetValueHigh: GetOptionalProperty<uint>(json, "secondary_custom_target_value_high")
            );
                messages.Add(message);
            }

            return messages;
        }

        private static WorkoutStepMesg CreateWorkoutStep(
            int messageIndex,
            string durationType,
            uint durationValue,
            string targetType,
            uint? targetValue = 0,
            uint? customTargetValueLow = null,
            uint? customTargetValueHigh = null,
            string? intensity = null,
            string? name = null,
            string? notes = null,
            string? secondaryTargetType = null,
            uint? secondaryTargetValue = 0,
            uint? secondaryCustomTargetValueLow = null,
            uint? secondaryCustomTargetValueHigh = null
        )
        {
            var workoutStepMesg = new WorkoutStepMesg();
            workoutStepMesg.SetMessageIndex((ushort)messageIndex);

            if (name != null) workoutStepMesg.SetWktStepName(name);
            if (notes != null) workoutStepMesg.SetNotes(notes);
            if (intensity != null) workoutStepMesg.SetIntensity(PropertyToEnum<Intensity>(intensity));
            if (durationType != null) workoutStepMesg.SetDurationType(PropertyToEnum<WktStepDuration>(durationType));
            if (durationValue > 0) workoutStepMesg.SetDurationValue(durationValue);
            if (targetType != null) workoutStepMesg.SetTargetType(PropertyToEnum<WktStepTarget>(targetType));
            if (targetValue != null) workoutStepMesg.SetTargetValue(targetValue);
            if (customTargetValueLow != null && customTargetValueHigh != null && customTargetValueLow > 0 && customTargetValueHigh > 0)
            {
                workoutStepMesg.SetCustomTargetValueLow(customTargetValueLow);
                workoutStepMesg.SetCustomTargetValueHigh(customTargetValueHigh);
            }
            if (secondaryTargetType != null) workoutStepMesg.SetSecondaryTargetType(PropertyToEnum<WktStepTarget>(secondaryTargetType));
            if (secondaryTargetValue != null && secondaryTargetValue > 0) workoutStepMesg.SetSecondaryTargetValue(secondaryTargetValue);
            if (secondaryCustomTargetValueLow != null && secondaryCustomTargetValueHigh != null && secondaryCustomTargetValueLow > 0 && secondaryCustomTargetValueHigh > 0)
            {
                workoutStepMesg.SetSecondaryCustomTargetValueLow(secondaryCustomTargetValueLow);
                workoutStepMesg.SetSecondaryCustomTargetValueHigh(secondaryCustomTargetValueHigh);
            }

            return workoutStepMesg;
        }
    }

}