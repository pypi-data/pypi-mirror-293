

class MailValidatorConfig:
    def __init__(self, config=None):
        # if config:
        #     self.blacklisted_domains = config.get("blacklisted_domains", [])
        #     self.whitelisted_domains = config.get("whitelisted_domains", [])
        #     self.blacklisted_emails = config.get("blacklisted_emails", [])
        #     self.whitelisted_emails = config.get("whitelisted_emails", [])
        # else:
        self.blacklisted_domains = []
        self.whitelisted_domains = []
        self.blacklisted_emails = []
        self.whitelisted_emails = []
