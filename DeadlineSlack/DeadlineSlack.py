from Deadline.Events import *
from functools import partial


def GetDeadlineEventListener():
    """Return the main DeadlineEventListener class
    
    Deadline calls this to get an instance of the main event listener.
    
    Returns:
        DeadlineEventListener: main event listener
    
    """
    return DeadlineSlackEvent()


def CleanupDeadlineEventListener(deadlinePlugin):
    """Called when deadline stops using the plugin.
    
    This is the function that Deadline calls when the event plugin is
    no longer in use so that it can get cleaned up.
    
    Returns:
        None
    
    """
    deadlinePlugin.cleanup()

    
class DeadlineSlackEvent(DeadlineEventListener):
    """Main event
    
    For each callback in CALLBACKS it will connect the
    relevant OnXXX() method on the instance.
    
    Upon clean-up each registered callback is removed.
    
    """
    
    CALLBACKS = [
        "OnJobFinished",
        "OnJobDeleted",
        "OnJobFailed",
        "OnJobPended",
        "OnJobReleased",
        "OnJobRequeued",
        "OnJobResumed",
        "OnJobPurged",
        "OnJobStarted",
        "OnJobSubmitted", 
        "OnJobSuspended",
        "OnJobError",
        "OnSlaveIdle",
        "OnSlaveStalled",
        "OnSlaveStarted",
        "OnSlaveStopped",
        "OnSlaveRendering",
        "OnSlaveStartingJob"
    ]
    
    def __init__(self):
        """Initialize the callbacks"""
        
        self.registered = []
        
        for name in self.CALLBACKS:
        
            # Connect the callback with the method
            callback = getattr(self, name + "Callback")
            callback += getattr(self, name)
            
            # Store as registered (connected callbacks)
            self.registered.append(name)
        
    def cleanup(self):
        """Cleanup the class and callbacks"""
        
        while self.registered:
            name = self.registered.pop()
            delattr(self, name + "Callback")
           
    # Define the callback class methods (they must be pre-defined)  
    def OnJobFinished(self, job):
        self.on_job("OnJobFinished", job)
        
    def OnJobDeleted(self, job):
        self.on_job("OnJobDeleted", job)
        
    def OnJobFailed(self, job):
        self.on_job("OnJobFailed", job)
        
    def OnJobPended(self, job):
        self.on_job("OnJobPended", job)
        
    def OnJobReleased(self, job):
        self.on_job("OnJobReleased", job)
        
    def OnJobRequeued(self, job):
        self.on_job("OnJobRequeued", job)
        
    def OnJobResumed(self, job):
        self.on_job("OnJobResumed", job)
        
    def OnJobPurged(self, job):
        self.on_job("OnJobPurged", job)
        
    def OnJobStarted(self, job):
        self.on_job("OnJobStarted", job)
        
    def OnJobSubmitted(self, job):
        self.on_job("OnJobSubmitted", job)
        
    def OnJobSuspended(self, job):
        self.on_job("OnJobSuspended", job)
        
    def OnJobError(self, job, task, report):
        self.on_job_error("OnJobError", job, task, report)
        
    def OnSlaveIdle(self, slave):
        self.on_slave("OnSlaveIdle", slave)
        
    def OnSlaveStalled(self, slave):
        self.on_slave("OnSlaveStalled", slave)
        
    def OnSlaveStarted(self, slave):
        self.on_slave("OnSlaveStarted", slave)
        
    def OnSlaveStopped(self, slave):
        self.on_slave("OnSlaveStopped", slave)
        
    def OnSlaveRendering(self, slave, job):
        self.on_slave_job("OnSlaveRendering", slave, job)
        
    def OnSlaveStartingJob(self, slave, job):
        self.on_slave_job("OnSlaveStartingJob", slave, job)
            
    def _get_message(self, key):
        """Get the message format for an Event
        
        Arguments:
            key (str): The name of the event.
            
        Returns:
            str: The unformatted message.
            
        """
        
        config_key = "Slack{0}Message".format(key)
        message = self.GetConfigEntryWithDefault(config_key, "")
        
        if message:
            # convert deadline event options multi line format
            message = message.replace(";", "\n")
        
        return message
        
    def on_job(self, key, job):
        """Callback for jobs.
        
        Related callbacks:
            OnJobFinishedCallback
            OnJobDeletedCallback
            OnJobFailedCallback
            OnJobPendedCallback
            OnJobPurgedCallback
            OnJobReleasedCallback
            OnJobRequeuedCallback
            OnJobResumedCallback
            OnJobStartedCallback
            OnJobSubmittedCallback
            OnJobSuspendedCallback
        
        Arguments:
            key (str): The message key
            job (Deadline.Jobs.Job): The job
            
        Returns:
            None
        
        """
        
        message = self._get_message(key)
        if message:
            self._post(message.format(job=job))
    
    def on_job_error(self, key, job, task, report):
        """Callback for job errors.
        
        Related callbacks:
            OnJobErrorCallback
        
        Arguments:
            key (str): The message key
            job (Deadline.Jobs.Job): Job that got an error
            task (Deadline.Jobs.Task): Task that raised the error
            report (Deadline.Reports.Report): Error report
            
        Returns:
            None
        
        """
        
        message = self._get_message(key)
        if message:
            self._post(message.format(job=job,
                                      task=task,
                                      report=report))
    
    def on_slave(self, key, slave):
        """Callback for slaves.
        
        Related callbacks:
            OnSlaveIdleCallback
            OnSlaveStalledCallback
            OnSlaveStartedCallback
            OnSlaveStoppedCallback
        
        Arguments:
            key (str): The message key
            slave (str): The slave name
            
        Returns:
            None
        
        """
        message = self._get_message(key)
        if message:
            self._post(message.format(slave=slave))
    
    def on_slave_job(self, key, slave, job):
        """Callback for slave jobs.
        
        Related callbacks:
            OnSlaveRenderingCallback
            OnSlaveStartingJobCallback
        
        Arguments:
            key (str): The message key
            slave (str): The slave name
            job (Deadline.Jobs.Job): The related job
            
        Returns:
            None
        
        """
        message = self._get_message(key)
        if message:
            self._post(message.format(slave=slave, 
                                      job=job))
        
    def _post(self, message):
        """Post message to Slack"""
        
        key = self.GetConfigEntryWithDefault("SlackAPIKey", None)
        if not key:
            return
        
        channel = self.GetConfigEntryWithDefault("SlackChannel", None)
        if not channel:
            return
            
        as_user = self.GetBooleanConfigEntryWithDefault("SlackAsUser", True)
        as_user = bool(as_user)
           
        from slacker import Slacker
        slack = Slacker(key)
        
        # Post to slack
        slack.chat.post_message(channel, 
                                message,
                                as_user=as_user)