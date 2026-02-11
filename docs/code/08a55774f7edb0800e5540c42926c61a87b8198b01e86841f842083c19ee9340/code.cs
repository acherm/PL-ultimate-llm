// Copyright (c) Microsoft Corporation
// The Microsoft Corporation licenses this file to you under the MIT license.
// See the LICENSE file in the project root for more information.

using System;
using System.Globalization;
using System.Text.Json.Serialization;
using System.Windows;
using ImageResizer.Properties;
using ImageResizer.Utilities;

namespace ImageResizer.Models
{
    public class ResizeSize
    {
        [JsonPropertyName("name")]
        public string Name { get; set; }

        [JsonPropertyName("width")]
        public double Width { get; set; }

        [JsonPropertyName("height")]
        public double Height { get; set; }

        [JsonPropertyName("unit")]
        public ResizeUnit Unit { get; set; }

        [JsonPropertyName("fit")]
        public ResizeFit Fit { get; set; }

        [JsonIgnore]
        public string Description
        {
            get
            {
                string unit = Unit switch
                {
                    ResizeUnit.Centimeter => Resources.Centimeter,
                    ResizeUnit.Inch => Resources.Inch,
                    ResizeUnit.Percent => Resources.Percent,
                    _ => Resources.Pixel,
                };

                string fit = Fit switch
                {
                    ResizeFit.Fill => Resources.Fill,
                    ResizeFit.Fit => Resources.Fit,
                    _ => Resources.Stretch,
                };

                return string.Format(
                    CultureInfo.CurrentCulture,
                    "{0} ({1})",
                    string.Format(
                        CultureInfo.CurrentCulture,
                        "{0} x {1} {2}",
                        Width,
                        Height,
                        unit),
                    fit);
            }
        }

        public Size GetPixelSize(int originalWidth, int originalHeight)
        {
            double width = 0;
            double height = 0;

            if (Unit == ResizeUnit.Percent)
            {
                width = originalWidth * Width / 100;
                height = originalHeight * Height / 100;
            }
            else
            {
                width = UnitConverter.ConvertToPixels(Width, Unit);
                height = UnitConverter.ConvertToPixels(Height, Unit);
            }

            if (Fit == ResizeFit.Fit)
            {
                double ratio = Math.Min(width / originalWidth, height / originalHeight);
                width = originalWidth * ratio;
                height = originalHeight * ratio;
            }
            else if (Fit == ResizeFit.Fill)
            {
                double ratio = Math.Max(width / originalWidth, height / originalHeight);
                width = originalWidth * ratio;
                height = originalHeight * ratio;
            }

            return new Size(Math.Max(1, width), Math.Max(1, height));
        }
    }
}