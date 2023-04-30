The Limiter plugin is a useful tool for protecting valuable resources from overloading or limiting the triggering of
some plugins. It works by stopping the execution of a workflow branch if a certain threshold is passed, such as 10
starts within one minute. To properly configure the plugin, we need to know what resource we are protecting and how we
identify it. For example, if we want to send emails to a specified email address but don't want the system to send more
than one email per day, the protected resource is the email address and the key that will identify the limiter is the
email address. We can also define a pair of keys, such as the email address and the email message, if we don't want the
customer to accidentally receive an email with the same content twice.

The limiter plugin also has an advanced JSON configuration, which includes keys that identify the throttle, the number
of allowed passes within a defined time, and the time to live for a throttle. The outputs of the plugin are "pass" and "
block", which trigger different ports depending on whether the executions are limited or not. It is important to note
that limiters placed in different workflows share the same information if they have the same key, meaning that
executions in one workflow will add up to the limit on the other workflow as well. To prevent this, we can add a
workflow id or custom key to the limiter key.