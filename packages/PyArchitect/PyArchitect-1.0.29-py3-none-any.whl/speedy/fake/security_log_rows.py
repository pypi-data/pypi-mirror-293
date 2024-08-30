# Define the events and their probabilities
import json
import random
from collections import deque
import threading
import time
from faker import Faker
from tqdm import tqdm

from speedy.fake.dates import get_working_past_date
from speedy.fake.users import generate_user_id_normal

class SecurityLogRows:
    _instance = None
    buffer = deque()
    batch_size = 0
    buffer_size = 0
    goal = 0
    count_generated = 0
    count_sent = 0
    buffer_pbar = None
    last_read_row = None       # Track the last read row or the beggining of the limit range
    last_delivered_row = None  # Track the last delivered row
    last_processed_row = None  # Track the last processed row
    reading_a_batch = False     # a semaphore to allow only one thread to read from database
    goal_row = 0
             
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SecurityLogRows, cls).__new__(cls)
        return cls._instance

    events = [
        ("ActivityReassignment", 2224),
        ("attempt", 578),
        ("AuthClientCreated", 80),   #=*10
        ("AuthClientDeleted", 50),   #=*10
        ("AuthClientUpdated", 60),   #=*10
        ("CollectionAccessed", 1524),  #=/1000
        ("CollectionCreated", 37),
        ("CollectionDeleted", 20),    #=*10
        ("CollectionRecordAccessed", 3167),
        ("CollectionUpdated", 80),   #=*10
        ("CustomizeUiUpdated", 40),  #=*10
        ("DataConnectorResourceAction", 47),
        ("EnvironmentVariablesCreated", 33),
        ("EnvironmentVariablesUpdated", 60),  #=*10
        ("FilesAccessed", 97),
        ("FilesCreated", 59460),
        ("FilesDeleted", 2892),
        ("FilesDownloaded", 53821),
        ("FolderAccessed", 15418),
        ("FolderCreated", 10),  #=*10
        ("GroupCreated", 60),   #=*10
        ("GroupMembersUpdated", 50),
        ("GroupUpdated", 36),
        ("login", 8495),
        ("logout", 2106),
        ("MenuCreated", 40),  #=*10
        ("MenuUpdated", 41),
        ("PermissionUpdated", 93),
        ("PmBlockArchived", 30),  #=*10
        ("ProcessArchived", 10),  
        ("ProcessCreated", 20),   #=*10
        ("ProcessUpdated", 4034),
        ("QueueManagementAccessed", 121),
        ("RecordCreated", 513),  #=/1000
        ("RecordDeleted", 217),
        ("RecordUpdated", 360), #=/1000
        ("RequestAction", 26178),
        ("RequestError", 7770), #=/100000
        ("SavedSearchChartCreated", 40),  #=*10
        ("SavedSearchChartDeleted", 20),  #=*10
        ("SavedSearchChartUpdated", 40),  #=*10
        ("SavedSearchCreated", 20),  #=*10
        ("SavedSearchDeleted", 11),
        ("SavedSearchUpdated", 110),
        ("ScreenCreated", 56),
        ("ScreenDeleted", 40),   #=*10
        ("ScreenUpdated", 2268),  
        ("ScriptCreated", 114),
        ("ScriptDeleted", 40),   #=*10
        ("ScriptDuplicated", 77),
        ("ScriptExecutorCreated", 30), #=*10
        ("ScriptExecutorUpdated", 53),
        ("ScriptUpdated", 3359),
        ("SettingsUpdated", 52),
        ("SignalCreated", 10), #=*10
        ("SignalUpdated", 30), #=*10
        ("TokenCreated", 51),
        ("UnauthorizedAccessAttempt", 5361),
        ("UserCreated", 157),
        ("UserDeleted", 56),
        ("UserGroupsUpdated", 659),
        ("UserRestored", 10),
        ("UserUpdated", 173)
    ]


    def init(self, goal, batch_size: int, buffer_size: int, pbar: tqdm):
        self.goal = goal
        self.batch_size = batch_size
        self.buffer_size = buffer_size
        self.buffer_pbar = pbar

    
    def init_fake_rows(self, goal, batch_size: int, buffer_size: int, pbar: tqdm):
        self.init(goal, batch_size, buffer_size, pbar)

        # Create a Faker instance
        self.fake = Faker()

        # Normalize the probabilities
        self.total = sum(weight for _, weight in self.events)
        self.events = [(self.event, weight/self.total) for self.event, weight in self.events]

        # set buffer
        self.buffer = deque(maxlen=self.buffer_size)
        for _ in range( int (self.buffer_size )):
            self.generate_a_batch()
            

    def fast_copy_init(self, goal, batch_size: int, buffer_size: int, pbar: tqdm, starting_row):
        self.init(goal, batch_size, buffer_size, pbar)

        # set the last 
        self.last_read_row = starting_row
        self.last_processed_row = starting_row
        self.last_delivered_row = starting_row
        self.starting_row = starting_row
        self.goal_row = starting_row + goal
        self.buffer_pbar.n = 0

        # set buffer
        self.reading_a_batch = False
        self.buffer = deque(maxlen=self.buffer_size*2)
        self.read_a_batch()


    def get_last_delivered_row(self):
        return self.last_delivered_row

    def get_last_processed_row(self):
        return self.last_processed_row

    def set_last_delivered_row(self, row):
        self.last_delivered_row = row

    def set_last_processed_row(self, row):
        self.last_processed_row = row
          
                
    def generate_a_batch(self):
        # generate one batch of fake rows and push into the queue
        # update the counters to make it available
        
        if self.count_generated >= self.goal: 
            return None
        
        this_batch_size = self.batch_size

        if self.count_generated + self.batch_size > self.goal:
            this_batch_size = max(0, self.goal - self.count_generated)
            
        batch = [self.generate_sl_row() for _ in range(this_batch_size)]
        
        self.count_generated += this_batch_size
        self.buffer.append(batch)
        self.buffer_pbar.n = len(self.buffer)
        self.buffer_pbar.refresh() 


    def get_batch_of_rows(self):
        # get the next available batch from the queue, 
        # if not available batch, waits until it is generated
        # do not wait, if no more batches to generate and return None
        # and then update the counters. 

        if not self.buffer and self.count_sent >= self.goal :
            while not self.buffer :
                time.sleep(0.1) # wait 0.1 second until the the buffer refills

        # get a batch and update counters
        if self.buffer:
            batch = self.buffer.popleft()
        else:
            return None
 
        # generate a batch in a separate thread
        if self.count_sent < self.goal:
            thread = threading.Thread(target=self.generate_a_batch)
            thread.start()

        self.buffer_pbar.n = len(self.buffer)
        self.buffer_pbar.refresh() 
        self.count_sent += 1

        return batch


    def get_batch_of_read_rows(self):
        # get the next available batch from the queue of read rows, 
        # if not available batch, waits until it is readed
        # do not wait, if reach the goal and return None
        # and then update the counters. 
        if not self.buffer and self.last_read_row < self.goal_row :
            while not self.buffer :
                time.sleep(0.1) # wait 0.1 second until the the buffer refills
                #print ("wait\n")
                    
        # return None if no more batches
        if not self.buffer:
            self.buffer_pbar.n = 0
            self.buffer_pbar.refresh() 
            return None 
            
        # get a batch and update counters
        batch = self.buffer.popleft()

        # read the next batch in a separate thread
        if self.last_read_row < self.goal_row and self.reading_a_batch == False:
            len_buffer = 0 if self.buffer is None else len(self.buffer)
            # start the thread when buffer is less of 50% of capacity
            if len_buffer < self.buffer_size:
                thread = threading.Thread(target=self.read_a_batch)
                thread.start()

        self.buffer_pbar.n = len(self.buffer)
        self.buffer_pbar.refresh() 
        self.last_delivered_row += len(batch)

        #print (f"\033[1A         {self.last_delivered_row} {self.goal}     \033[1B", end='') 
        #tqdm.write (f"   {self.last_delivered_row} {self.goal}  ", end='') 
        return batch
    

    def read_a_batch(self):
        # read a batch from database, executes only one tread, no parallelism
        self.reading_a_batch = True
        
        # Logic to read the next batch of rows from the table
        time.sleep(0.5)
        this_buffer_size = self.buffer_size
        pending_rows = self.goal_row - self.last_read_row 
        if  pending_rows < self.buffer_size * self.batch_size:
            this_buffer_size, last_batch_size = divmod (pending_rows, self.batch_size)

        for i in range(this_buffer_size):
            batch = []
            for i in range(self.batch_size):
                batch.append ( {"n":i*100, "data": "ABC"} )
            
            self.buffer.append(batch)                
        
        self.last_read_row += this_buffer_size * self.batch_size
        
        if this_buffer_size != self.buffer_size:
            last_batch = []
            for i in range(last_batch_size):
                last_batch.append ( {"n":i*100, "data": "last"} )
            
            self.buffer.append(last_batch)                
            self.last_read_row += 1 * last_batch_size

        self.buffer_pbar.n = len(self.buffer)
        self.buffer_pbar.refresh() 
        self.reading_a_batch = False
        
        
    def multipleInserts(self):
        return (
            "INSERT INTO security_logs "
            "(event, ip, meta, user_id, data, changes, occurred_at) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        
        
    # generate a fake row
    def generate_sl_row(self):
        event = random.choices(*zip(*self.events))[0]
        ip = self.fake.ipv4()
        user_id = generate_user_id_normal(5000)  
        occurred_at = get_working_past_date(1000, 10)
        
        meta = json.dumps({
            "os": {
                "name": self.fake.random_element(elements=('Windows', 'Linux', 'MacOS')),
                "version": self.fake.random_number(digits=2)
            },
            "browser": {
                "name": self.fake.random_element(elements=('Chrome', 'Firefox', 'Safari', 'Edge', 'Opera', 'PHP', 'Postman')),
                "version": str(self.fake.random_number(digits=2))
            },        
            "user_agent": self.fake.user_agent()
        })
        data, changes = self.generate_value_for_event(event)
        return (event, ip, meta, user_id, data, changes, occurred_at)


    # generate fake value for specific columns
    def generate_value_for_event(self, event: str):

        if event == 'ActivityReassignment':
            process_id = random.randint(100,200)
            request_id = random.randint(100,900)
            return json.dumps( {
                "task": "Validation Backlog", 
                "process": "Client Instruction Process", 
                "request": {
                    "link": f"https://intembeko.cloud.processmaker.net/requests/{request_id}", 
                    "label": request_id
                }, 
                "name_action": "REASSIGNMENT", 
                "actionated_at": get_working_past_date(1000, 10)
            }), json.dumps({
                "process_id": process_id,
                "request_id": request_id
            })
                    
        if event == 'attempt':
            return None, None
                    
        if event == 'AuthClientCreated':
            return json.dumps( {
                "name": {
                    "link": f"https://intembeko.cloud.processmaker.net/admin/auth-clients", 
                    "label": "Coronation API LOCAL"
                }, 
                "revoked": False, 
                "process": "Client Instruction Process", 
                "provider": "", 
                "redirect": "", 
                "created_at": get_working_past_date(1000, 10),
                "personal_access_client": False
            }), json.dumps({
                "id": random.randint(100,1000),
                "user_id": random.randint(100,1000)
            })
                    
                    
        if event == 'AuthClientDeleted':
            id = random.randint(1,100)
            return json.dumps( {
                "name": "Coronation API LOCAL", 
                "auth_client_id": id, 
                "deleted_at_at": get_working_past_date(1000, 10)
            }), json.dumps({
                "id": id, 
                "name": "Coronation API LOCAL", 
                "secret": "ercCOxBqmc5Bg8zqXF4gRXIjjb9sA0CkLJuB2yX2", 
                "revoked": True, 
                "user_id": random.randint(100,1000),
                "provider": None, 
                "redirect": "http://localhost", 
                "created_at": get_working_past_date(1000, 10), 
                "updated_at": get_working_past_date(1000, 10), 
                "password_client": 1, 
                "personal_access_client": 0
            })
                    
                    
        if event == 'RequestError':
            id = random.randint(1,10000)
            return json.dumps( {
                "id": id, 
                "request": {
                    "label": random.randint(1,5000) + 1000,
                    "link": "https://intembeko.cloud.processmaker.net/requests/6865"
                },
                "error": "ProcessMaker\\Jobs\\CompleteActivity::action(): Argument #1 ($token) must be of type ProcessMaker\\Models\\ProcessRequestToken, null given, called in /opt/processmaker/vendor/laravel/framework/src/Illuminate/Container/BoundMethod.php on line 36",
                "accessed_at": get_working_past_date(1000, 10)
            }), None
                                                               
        
        if event == 'CollectionAccessed':
            id = random.randint(1,100)
            return json.dumps( {
                "id": id, 
                "name": {
                    "link": f"https://intembeko.cloud.processmaker.net/collections/{id}", 
                    "label": self.fake.random_element(elements=('CIP_ERROR_CATEGORIES', 'CIP_PRODUCT','CIP_CLIENT', 'CIP_HR_ADMIN', 'CIP_FOLDERS', 'CIP_MANAGERS'))
                }, 
                "accessed_at": get_working_past_date(1000, 10)
            }), json.dumps({
                id: id
            })

        
        id = random.randint(1,100)
        return json.dumps( {
            "id": random.randint(1,100000) + 10000
        }), json.dumps({
            id: id
        })

        