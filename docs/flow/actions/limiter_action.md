# Limiter plugin

The plugin limits the number of launches to a certain number in a given period of time. It is perticualry usefull when we would like to protect valuable resources from overloading or limit the triggering of some plugins. 

You have to remember that some events maybe triggered very fast and process time of a event may be longer then the time between the event triggers. That may casuse the workflow to run server times. Is such case a throttle (limiter) may be used to limit the number of executions.

It works ina a way that stops execution of a workflow branch if some threshold is passed, for example, 10 starts within one minute. The workflow will work untill 10 executions are completed and then will throttle the rest of the executions until one minute end (or other defined time range).

# Configuration

In order to properly configure the plugin, we need to know what resource we are protecting and how we identify it. Let's assume that we want to send e-mails to the specified e-mail address. However, we don't want the system to send more than one email per day. Regardless  the email's message. In this case, the protected resource is email. Therefore, the key that will identify our limiter (throttle) will be the e-mail address. You can define a pair of keys. e.g. if we do not want the customer to accidentally receive an email with the same content twice, we can set the key for the email and the e-mail message.

The order of throttle keys is impoertant, because this is the way the limiter identifies the protected resource.

# Side effects

The limiters placed in different workflows share the same information if they have he same key. That means if we send emails in many workflow and throttle/limit the number executions based on email - execution in one workflow 
will add up to the limit on the other workflow as well. This is a very powerful feature that can protect resources across all workflows if set properly.

If you want the limiter to work only for one workflow and not across all workflows add workflow id to a limiter key,
e.g. workflow.id + email.

