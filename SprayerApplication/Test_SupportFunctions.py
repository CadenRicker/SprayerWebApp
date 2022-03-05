from pickle import TRUE
import unittest
from supportFunctions import *
from SQLtables.SprayData.sql import run
from flask import Flask, render_template, request, redirect, url_for, session
import config
class Test_SupportFunctions(unittest.TestCase):
	def setUp(self):
		run('SQLtables/SprayData/SprayData.xlsx') # initializes the database		
		return super().setUp()
	def test_sortByList(self):
		list1 = [1,2,4,3]
		list2 = ['d','c','a','b']
		resultOfFunc = sortByList(list1=list1, list2=list2)
		expected = ['a','b','c','d']
		self.assertEqual(expected,resultOfFunc)
	def test_filtterQuerry(self):
		result =[['2 4-d lv 4 winfield united','dandelion',21.00],
		['2 4-d amine 4 albaugh','bitterweed',31.00],
		['2 4-d amine 4 albaugh','broomweed',31.00],
		['2 4-d amine 4 albaugh','dandelion',31.00],
		['2 4-d amine alligare  llc','bitterweed',20.00],
		['2 4-d amine alligare  llc','broomweed',20.00],
		['2 4-d amine alligare  llc','dandelion',20.00],
		['dagger','dandelion',10.00]]
		resultOfFunc = filterQuery(result)
		expected = [['2 4-d amine alligare  llc', '20.00', ['bitterweed', 'broomweed', 'dandelion']],
					['2 4-d amine 4 albaugh', '31.00', ['bitterweed', 'broomweed', 'dandelion']], 
					['dagger', '10.00', ['dandelion']], ['2 4-d lv 4 winfield united', '21.00', ['dandelion']]]
		self.assertEqual(expected,resultOfFunc)
	def test_CalculateResult(self):
		sprayName ='2 4-d amine alligare  llc'
		sprayData = [['2 4-d amine alligare  llc', '20.00', ['dandelion', 'broomweed', 'bitterweed'], '2.00'],
					 ['2 4-d amine 4 albaugh', '31.00', ['dandelion', 'broomweed', 'bitterweed'], '1.70'],
					 ['dagger', '10.00', ['dandelion'], '1.15'],
					 ['2 4-d lv 4 winfield united', '21.00', ['dandelion'], '2.10']]
		acerage = 10
		sprayGPA = 11
		tankSize = 100
		resutultOfFunc = calculateResult(sprayName,sprayData,acerage,sprayGPA,tankSize)
		expected =[sprayName,2.5,50.00,[1,2.2727],[0.2273,9.7727]]
		self.assertEqual(expected , resutultOfFunc)
if __name__ == '__main__':
	unittest.main()