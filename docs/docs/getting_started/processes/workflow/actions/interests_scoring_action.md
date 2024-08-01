# Interest scoring

This plugin calculates a normalized value of interests using the exponential decay over time. It applies a decay
function to decrease the magnitude of each interest over time and then normalizes these values using a softmax function
to emphasize the most significant interests.

# Version

0.9.0

## Description

The Interest Scoring Action plugin evaluates the decay of interests over time. This decay is based on a mathematical
model where the interest magnitude decreases exponentially based on a defined decay rate and the elapsed time since the
interest was last updated. The plugin retrieves timestamps for each interest from a user's profile, computes the decayed
interest scores, and then applies a softmax function to normalize these scores. The result highlights the most prominent
interests relative to others. The top interest along with its probability score is also identified and returned.

### Details

Interest scores are calculated using a decay function, specifically an exponential function that reduces the interest
magnitude over time. This reduction is based on the formula: magnitude × e^(-decay × time_passed), where "e" represents
the exponential function. The scores are subsequently normalized with a softmax function, which emphasizes the most
significant interest by giving it the highest value.

For instance, if the initial interest magnitude is 1 with a decay factor of 0.1, the interest will nearly disappear (
approach a value of 0) after 14 time units - these units could be seconds, minutes, etc.

In another scenario, if the interest starts with value 10, then after 14 days, it would reduce to approximately 2.46.
Additionally, there is always a baseline interest labeled "unknown" with a fixed magnitude of 0.5. If any interest's
magnitude falls below 0.25, its calculated score will then be set to zero.

This plugin is particularly useful when you want to quantify the decline in customer interest over time and identify the
most current prominent interest. If multiple interests are equally significant, the probability is evenly distributed
among them. The total probability across all interests will always sum up to 1.

# Inputs and Outputs

- __Inputs__: This plugin requires a payload object as input which includes user profile details necessary for
  calculating interest decay.
- __Outputs__: The plugin outputs the scoring results for each interest, including the list of all interests with their
  respective decayed values and the top interest with its probability score.

## Examples

### Output Example

```json
{
  "scoring": {
    "unknown": 0.1,
    "reading": 0.6,
    "sports": 0.3
  },
  "interests": {
    #
  Current
  interest
  values
  "unknown": 0.5,
  "reading": 7,
  "sports": 5
},
"top": "reading",
"probability": 0.6
}
```

# Configuration

- __Decay factor__: This is the rate at which the interest should decrease over time.
- __Time unit__: What is the smallest unit of time that should reduce the interest value? Options include seconds,
  minutes, hours, days, or months.

# JSON Configuration

```json
{
  "decay": 0.1,
  "base": "60"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Prerequisites

This plugin works with build-in event types (Increase Interest, Decrease Interest, Reset Interest) and does not
specifically require synchronous events.

# Side effects

This plugin will update profile (field: metadata.fields) if the last timestamp if any of the interests is missing. The
timestamp will be set to current date and time.

# Errors

- __Profile event sequencing can not be performed without profile. Is this a profile less event?__ - This error occurs
  if the plugin attempts to access the profile's interests or metadata but the profile data is missing in the payload.
  Ensure that the payload includes profile information before running this plugin.