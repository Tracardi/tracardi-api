This plugin allows users to perform simple operations such as addition, subtraction, division, and multiplication. The arguments of these operations can be values from the payload, profile, etc. The result of the operation is returned as an object of new values. Each operation must be in a separate row and operations may share variables. 

For example, the equation `profile@traits.private.interests.sports =  profile@traits.private.interests.sports / payload@time_passed` will divide the value from the profile located in `traits.private.interests.sports` by the number provided in the payload (time_passed). The result of this equation will be an object with the result and variables. 

Variables can also be used in calculations. For example, the equation `decay_rate = 2; result.value = profile@traits.private.interests.sports / decay_rate` will assign a value to the variable `decay_rate` and then use this value to compute `result.value`. The result of this equation will be an object with the result and variables. 

Compound calculations can also be performed. For example, the equation `a = 1 + 2 / 3; b = (1 + 2) / 3; c = a + b` will return an object with the result and variables. Each number can be replaced by a variable or a field from the profile, event, etc. 

Negative values can also be calculated. For example, the equation `event@counter = 1; -event@counter` will return an object with the result and variables. The result of this equation will be -1 and the event@counter will equal 1.