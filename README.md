# AT as Aiven Test

## Pre-requirements
 * docker
 * docker-compose
 * git
 * internet access(it can take couple of GB, so if you are on the mobile internet - consider this)



## Usage instructions:


### 1. Clone this repo
 ```bash
$ git clone git@github.com:darnes/at.git
 ```

### 2. Change dir to `at` and execute 
```bash
$ cd at
$ ./run_me.sh
 ```
 And let docker work for you. 
 
### 3. Wait
It could take up to 10 mins until you'll see messages like this:
```bash
consumer_1  | DEBUG:pykafka.simpleconsumer:Fetched 1 messages for partition 0
consumer_1  | DEBUG:pykafka.simpleconsumer:Partition 0 queue holds 1 messages
consumer_1  | DEBUG:dshw.consumer:cpu: 100.0, time 2019-11-14 08:07:30.838945, fullmsg: b'{"cpu_usage": 100.0, "mem_usage": 95.7, "timestamp": "2019-11-14 08:07:30.838945"}'
producer_1  | DEBUG:pykafka.producer:Successfully sent 1/1 messages to broker 0
producer_1  | DEBUG:dshw.producer:producing message 2019-11-14 08:07:31.953384
```

that means all good and you can carry on to next stage. 

### 4. Verify
In order to verify that all works as expected.
Open new terminal window, and cd to same place you end up at stage 2.
Then perform following sequence of commands:
```bash
$ docker-compose exec postgres bash
root@82ce05efb9e4:/# su postgres
postgres@82ce05efb9e4:/$ psql 
psql (12.0 (Debian 12.0-2.pgdg100+1))
Type "help" for help.

postgres=# \c monitor
You are now connected to database "monitor" as user "postgres".
monitor=# select * from metric order by timestamp DESC limit 10;

```

if you see something like
```bash
monitor=# select * from metric order by timestamp DESC limit 10;
 id  | cpu_usage | mem_usage |         timestamp          
-----+-----------+-----------+----------------------------
 535 |       2.6 |      85.8 | 2019-11-14 08:17:14.597224
 534 |         0 |      85.8 | 2019-11-14 08:17:13.485794
 533 |       2.6 |      85.6 | 2019-11-14 08:17:12.377462
 532 |       2.6 |      85.6 | 2019-11-14 08:17:11.267322
 531 |      12.2 |      85.6 | 2019-11-14 08:17:10.154706
 530 |      42.1 |      85.7 | 2019-11-14 08:17:09.044896
 529 |         0 |      85.5 | 2019-11-14 08:17:07.936204
 528 |         0 |      85.5 | 2019-11-14 08:17:06.826374
 527 |       7.5 |      85.5 | 2019-11-14 08:17:05.715638
 526 |       2.6 |      85.5 | 2019-11-14 08:17:04.592806
```

And with every call timestamp keep changing means that I was successful and can carry on to the next stage.

### 5. Celebrate
Best way to celebrate is to provide feedback, please do not hesitate to contact me and tell me what you liked and especially what you do not like. 

### 6. Cleanup
If you reading this and went that far most likely you know what to do. 
Just as extra precaution here are steps:
 1. Stop process started at step 2 (Control+C)
 2. Run `docker-compose down` to remove containers. 
 3. Now you will have few images you will need to cleanup.
  Command `docker image rm ` is your best friend.

# Credits

Local kafka docker image:
https://github.com/lensesio/fast-data-dev

Google.
Used mostly for the kafka connection stuff.