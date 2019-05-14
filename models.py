#This file controls all the music logic

from controller import compute_transition_time, play_fret, go_to, amp_on, amp_off, release_HW, mrduck, setup_picks
import threading
import time

#useful function for modding with no negative output
def my_mod(a, n):
	return ((a%n) + n) % n

#Class that contains information about a note (time, fret and string)
class Note:

	WHOLE       = 0
	HALF_DOT    = 1
	HALF        = 2
	QUARTER_DOT = 3
	QUARTER     = 4
	EIGHTH      = 5

	def __init__(self, fret, string, note_type):
		self.fret = fret
		self.string = string
		self.note_type = note_type

	@staticmethod
	def compute_note_time(note, bpm):
		single_beat = 60/bpm
		if (note.note_type == Note.WHOLE):
			return 4*single_beat
		elif (note.note_type == Note.HALF_DOT):
			return 3*single_beat
		elif (note.note_type == Note.HALF):
			return 2*single_beat
		elif (note.note_type == Note.QUARTER_DOT):
			return 1.5*single_beat
		elif (note.note_type == Note.QUARTER):
			return single_beat
		elif (note.note_type == Note.EIGHTH):
			return 0.5*single_beat
		return 4*single_beat

#A controller that can play a song that is passed to it
class SongPlayer:

	def __init__(self):
		self.current_song = None
		self.note_index = -1
		self.loop = 1
		self.end = False
		self.ready = True

	def rec_play(self, song):
		#Play next note
		print("play next note")
		self.note_index+=1
		if (self.note_index >= len(song.notes)):
			self.loop -= 1
			if (self.loop > 0):
				self.note_index = 0
			else:
				self.ready = True
				return
		current_note = song.notes[self.note_index]

		#Compute the time between this note and the next
		note_time = Note.compute_note_time(current_note, song.bpm)
		print("note duration:"+str(note_time))
		#Compute the time to travel from this note to the next
		next_note = current_note
		if self.note_index+1 < len(song.notes):
			next_note = song.notes[self.note_index+1]
			trans_time = compute_transition_time(next_note.fret, next_note.string)
		else:
			trans_time = 0
		#Compute time permitted to ring to "guarantee" arrival to next note on time
		ring_time = note_time - trans_time
		print("computed ring time: "+str(ring_time))
		if ring_time < 0:
			print("TOO FAST FOR STEPPER!")
			ring_time = 0
		#Rest if the current sound is less than zero
		if (current_note.fret >= 0):
			print("Playing fret:"+str(current_note.fret)+" String:"+str(current_note.string))
			play_fret(current_note.fret, current_note.string, ring_time)
		else:
			print("playing rest note")
			time.sleep(ring_time)
		print("end of this note")
		self.rec_play(song)

	def play(self, song):
		#Can only play non-None songs
		if song is None:
			print("ERROR: attempting to play a 'NONE' song")
			return
		#Only play if ready
		if self.ready:
			amp_on()
			self.ready = False
			self.note_index = -1
			self.current_song = song
			self.loop = song.loop
			self.rec_play(song)
			release_HW()
			amp_off()
			mrduck()
			go_to(0)
			setup_picks()

#Wrapper class for a song. Basically a collection
#of notes with a bpm and loop count.
class Song:

	def __init__(self, notes, bpm):
		self.notes = notes
		self.bpm = bpm
		self.loop = 1

#Test song
test = Song([Note(2,0,Note.QUARTER), Note(5,0,Note.QUARTER), Note(7,0,Note.QUARTER),
		Note(2,0,Note.QUARTER), Note(5,0,Note.QUARTER), Note(8,0,Note.QUARTER), Note(7,0,Note.QUARTER),
		Note(2,0,Note.QUARTER), Note(5,0,Note.QUARTER), Note(7,0,Note.QUARTER),
		Note(5,0,Note.QUARTER), Note(2,0,Note.QUARTER)], 30)

#Pachelbel's first section
section1 = [Note(2,2,Note.QUARTER), Note(2,1,Note.QUARTER), Note(4,1,Note.QUARTER),
		Note(4,0,Note.QUARTER), Note(0,1,Note.QUARTER), Note(0,0,Note.QUARTER),
		Note(0,1,Note.QUARTER), Note(2,1,Note.QUARTER)]

pachelbel = Song(section1, 40)
pachelbel.loop = 2

#Happy birthday by section
birthday1 = [Note(2,1,Note.EIGHTH), Note(2,1,Note.EIGHTH), Note(4,1,Note.QUARTER), Note(2,1,Note.QUARTER), Note(2,2,Note.QUARTER), Note(6,1,Note.QUARTER)]
birthday2 = [Note(2,1,Note.EIGHTH), Note(2,1,Note.EIGHTH), Note(4,1,Note.QUARTER), Note(2,1,Note.QUARTER), Note(4,2,Note.QUARTER), Note(2,2,Note.QUARTER)]
birthday3 = [Note(2,1,Note.EIGHTH), Note(2,1,Note.EIGHTH), Note(2,3,Note.QUARTER), Note(4,2,Note.QUARTER), Note(7,1,Note.QUARTER), Note(6,1,Note.QUARTER), Note(4,1,Note.QUARTER)]
birthday4 = [Note(0,3,Note.EIGHTH), Note(0,3,Note.EIGHTH), Note(4,2,Note.QUARTER), Note(7,1,Note.QUARTER), Note(9,1,Note.QUARTER), Note(7,1,Note.QUARTER)]

birthday = Song(birthday1+birthday2+birthday3+birthday4, 40)
birthday.loop = 1

#List of available songs
song_map = [ pachelbel, birthday, test ]

#player to play songs
song_player = SongPlayer()

#Function used to perform a selected song
def play_song(song_index):
	global song_map, song_player
	song_player.play(song_map[song_index])
