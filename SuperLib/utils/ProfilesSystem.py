import os, json
from .utils import get_unix_timestring, get_unix_timestamp
PROFILES_REL_PATH = "./Profiles"
PROFILES_FOLDER = PROFILES_REL_PATH
##PROFILES_FOLDER = os.path.join(os.path.dirname(__file__), PROFILES_REL_PATH)
# if not os.path.is_dir(PROFILES_FOLDER):
#   os.makedirs(PROFILES_FOLDER,exist_ok=True)

def get_profiles_folder():
    """Gets the absolute path to the included profiles folder. `Returns a String`"""
    return os.path.abspath(PROFILES_FOLDER)

def get_profiles_list(path=PROFILES_REL_PATH, verbose=False):
    """Gets a list of profile files at a given path. `Returns a List of Path strings`"""
    profiles = []
    for entry in os.scandir(path):
        if entry.is_file():
            if entry.path.endswith("_meta.json"):
                profiles.append(os.path.abspath(entry.path))
    if verbose:
        print(f"Found {len(profiles)} user profiles: {json.dumps(profiles, indent=4)}")
    return profiles

class UserProfile:
    """A class to represent a User / User's Preferences"""
    __desc__ = """Must pass a unique username and a unique identifier for new profile."""
    def __init__(self, path, username:str=None, atomic:str=None):
        self.path = path
        self.username = username
        self.atomic = atomic
        if os.path.isfile(self.path):
            self.load()
        elif os.path.isdir(self.path): 
            #Path is a dir for new object
            ts = get_unix_timestamp()
            self.path = os.path.join(path, atomic)+"_meta.json"
            self.data = {
                "username":username,
                "atomic":atomic,
                "preferences":{},
                "last_edited":ts,
                "last_accessed":ts,
            }
            self.save()
        else:
            raise FileNotFoundError("User path not found.")

    def save(self):
        with open(self.path, "w+") as f:
            json.dump(self.data, f, indent=4)

    def load(self):
        with open(self.path) as f:
            self.data = json.load(f)
        self.username = self.data["username"]
        self.atomic = self.data["atomic"]

    def set_username(self, name:str):
        self.username = name
        self.data["username"]=name
        self.save()

    def set_preference(self, key:str, value:str):
        self.data["preferences"][key]=value
        self.save()

    def get_preference(self, key:str):
        return self.data["preferences"].get(key,None)

    def clear_preferences(self, preferences:list=None):
        if preferences:
            for p in preferences:
                self.data["preferences"].pop(p)
        else:
            self.data["preferences"] = {}
        self.save()

class ProfilesSystem:
    def __init__(self, select_profile_actions:list=[], refresh_profiles_actions:list=[], profiles_dir:str=get_profiles_folder(), handle_duplicates:bool=True):
        """select_profile_actions is a list of callbacks to call when the selected profile changes."""
        self.select_profile_actions = select_profile_actions
        self.refresh_profiles_actions = refresh_profiles_actions
        self.profiles_dir = profiles_dir
        self.current_profile = None
        self.profiles = []
        
        if os.path.isdir(self.profiles_dir):
            profile_names = []
            duplicate_names = []
            for u in get_profiles_list(self.profiles_dir, verbose=True):
                user = UserProfile(u)
                if user.username in profile_names:
                    duplicate_names.append(user.username)
                else:
                    profile_names.append(user.username)
                self.profiles.append(user)
            if handle_duplicates:
                for name in duplicate_names:
                    self.handle_duplicate_profile_names(name)
        else:
            #Init profile directory
            os.makedirs(self.profiles_dir, exist_ok=True)
            
        if self.profiles:
            self.current_profile = self.profiles[0]
        else:
            self.create_profile("Default")
        self.clear_select_profile_actions(self.select_profile_actions)

    def add_select_profile_action(self, action):
        """Add an action to the profile switch actions"""
        self.select_profile_actions.append(action)
    def add_select_profile_actions(self, actions:list):
        """Add a list of actions to the profile switch actions"""
        self.select_profile_actions.extend(actions)
    def clear_select_profile_actions(self, new:list=[]):
        """Clear out the profile switch actions, optionally replacing them with new ones"""
        self.select_profile_actions=new.copy()
    def handle_select_profile_actions(self):
        """Handle on-profile-selection actions"""
        for action in self.select_profile_actions:
            action(self.current_profile)
            
    def add_refresh_profiles_action(self, action):
        """Add an action to the profiles list refresh actions"""
        self.refresh_profiles_actions.append(action)
    def add_refresh_profiles_actions(self, actions:list):
        """Add a list of actions to the profiles list refresh actions"""
        self.refresh_profiles_actions.extend(actions)
    def clear_refresh_profile_actions(self, new:list=[]):
        """Clear out the profiles list refresh actions, optionally replacing them with new ones"""
        self.refresh_profiles_actions=new.copy()
    def handle_refresh_profiles_actions(self):
        """Handle on-refresh-profiles actions"""
        for action in self.refresh_profiles_actions:
            action(self.current_profile)
    
    def select_profile(self, profile:UserProfile):
        """Change the currently selected profile"""
        if not profile:
            raise ValueError(f"Profile cannot be Nonetype.")
        if not profile in self.profiles:
            raise ValueError(f"Supplied profile not in profiles system.")
        self.current_profile = profile
        profile.data["last_accessed"]=get_unix_timestamp()
        profile.save()
        self.handle_select_profile_actions()

    def get_profile_by_username(self, name: str):
        print(f"Looking for profile - {name}")
        prof = None
        for p in self.profiles:
            if p.username == name:
                prof = p
                break
        if prof:
            return prof
        else:
            raise ValueError(f"Unable to find profile")


    def select_profile_by_username(self, name:str):
        self.select_profile(self.get_profile_by_username(name))

    def create_profile(self, name:str):
        """Creates a profile with a given name. `Raises ValueError` if the profile name already exists. `Returns a UserProfile`"""
        for p in self.profiles:
            if p.username == name:
                raise ValueError(f"A profile of name {name} already exists.")
        self.current_profile = UserProfile(self.profiles_dir, name, get_unix_timestring())
        self.profiles.append(self.current_profile)
        return self.current_profile
        
    def sort_profiles_by_accessed(self, profiles:list=None):
        """Sort a list of profiles by last accessed, if no list is provided returns a sorted list of all profiles in the system. `Returns a List`"""
        profiles = profiles or self.profiles
        return list(reversed(sorted(profiles, key = lambda x:float(x.data["last_accessed"]))))

    def get_last_used_profile(self, profiles:list=None):
        """Returns the most recently accessed profile"""
        profiles = profiles or self.profiles
        return self.sort_profiles_by_accessed(profiles)[0] if profiles else None

    def check_if_name_exists_in_profiles(self, name:str, profiles:list=None):
        """Check if a name exists in a list of profiles, if no list is provided uses the list of all profiles. `Returns a Bool`"""
        profiles = profiles or self.profiles
        names = [p.username for p in profiles]
        return name in names

    def handle_duplicate_profile_names(self, name:str):
        """Makes profile names unique if they have identical names. \
The most recently accessed profile (according to the file json) keeps \
its name untouched. `Returns None`"""
        print(f"Handling duplicates of name - {name}")
        profiles_with_duplicate_names = []
        for p in self.profiles:
            if p.username == name:
                profiles_with_duplicate_names.append(p)
        if not profiles_with_duplicate_names:
            print(f"No profiles found with name matching - {name}")
            return
        if len(profiles_with_duplicate_names) == 1:
            print(f"Only one profile of name - {name} - was found.")
            return
        # Get most recently used profile
        recent = self.get_last_used_profile(profiles_with_duplicate_names)
        index = 2
        for p in profiles_with_duplicate_names:
            # Make sure it's not the most recently accessed
            if not p is recent:
                while True:
                    new_name = f"{p.username} {index}"
                    if not self.check_if_name_exists_in_profiles(new_name):
                        print(f"\tChanging username for profile at {p.path} to {new_name}")
                        p.set_username(new_name)
                        break
                    index += 1
        self.profiles=self.sort_profiles_by_accessed()

    def get_profile_names(self):
        """Returns an alphabetically sorted list of profile names"""
        return list(sorted(p.username for p in self.profiles))

    def delete_profile(self, profile:UserProfile):
        if not profile in self.profiles:
            raise ValueError("Attempted to delete profile that is not in the profiles list.")
        if profile is self.current_profile:
            raise ValueError("Attempted to the currently selected profile. Make a new profile in order to delete this one.")
        self.profiles.remove(profile)
        os.remove(profile.path)
        self.handle_refresh_profiles_actions()
        
        

    

PROFILES_OBJECTS = [
    ProfilesSystem,
    UserProfile,
]
PROFILES_FUNCTIONS = [
    get_profiles_folder,
    get_profiles_list,
]
