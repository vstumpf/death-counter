# Death Counter
This is a death counter.
When you hit a hotkey, it adds a death and increments the count.
Simple, right?

It could really be used as any counter, but the VCs who funded this project needed a death counter.
If it really bothers you that much, you can fork this project and make a PR.
They got what they wanted.

# Configuration
First of all, set up your configuration.
Copy `deathcounter.ini.example` to `deathcounter.ini` and customize it. 

## Twitch
This has everything that is related to Twitch.

### Username
This is your twitch username.
It should be really simple to find this.
You should know it.

If you need help with this, I'm sorry.
You should probably just stop now.

### Client-ID
This is how we get the currently playing game from Twitch.

For the name of your application, it doesn't really matter.
I'd call it Death Counter.
But that's just me.

For the Redirect URI, just put `http://localhost`.
It doesn't really matter either.

For the Application Category, literally anything is ok.
Choose a random one.
I dare you.

OR, if you didn't like that tutorial, check out [Generating and Setting a Twitch Client ID](https://docs.aws.amazon.com/lumberyard/latest/userguide/chatplay-generate-twitch-client-id.html).
It's from the same people who own Twitch!

## Hotkeys
The fun part!
This is where you set up your hotkeys.

The defaults are pretty explanitory.
If you need more help, check out [keyboard](https://github.com/boppreh/keyboard)!
That's the module I'm using!

### RecordDeath
The hotkey to record a death.

### UndoDeath
The hotkey that undos a death.
(undoes? uno dos? idk)

It removes the last death recorded.
Good if you accidently hit the death key.

## Paths
Back to boring things.
It's pretty much just filenames.

### Database
The filename of the database.
Just leave this alone.
Don't change it in the middle.
That'd be a bad idea.

### OBSSource
The filename of the total count.
This is the file with the number of total deaths.
It gets updated every time you record or undo a death.
Point OBS to this.

## Disclaimers
I wrote this during Christmas break, trying to hide away from family.
If there's any problems, blame it on the them.