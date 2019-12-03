import sys

CLUSTER_SPOTS = [0, 79, 75, 32]
CLUSTER_ROWS = [[],
                [0, 11,  6,  9, 11, 21, 21],
                [0, 12, 13, 13, 12, 13, 13],
                [0,  7,  7,  6,  6,  6]]

PH_USERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&"

"""
Assumptions:
Only 1 cluster per exam (easy to change)
Goal is maximum separation
  (IMO a separation of 3 (2 iMacs + facing seat) is perfect and easier to supervise)
All rows are perfect and equal
"""

"""
Sample outputs:
Number of users: 43
Cluster: 2
[0]
[8, 'A', 'G', 'B', 'H', 'C', '.', 'D', '.', 'E', '.', 'F', '.']
[7, 'I', '.', 'J', '.', 'K', '.', 'L', '.', 'M', '.', 'N', '.', 'O']
[7, 'P', '.', 'Q', '.', 'R', '.', 'S', '.', 'T', '.', 'U', '.', 'V']
[7, 'W', '3', 'X', '.', 'Y', '.', 'Z', '.', '1', '.', '2', '.']
[7, '4', '.', '5', '.', '6', '.', '7', '.', '8', '.', '9', '.', '0']
[7, '!', '.', '@', '.', '#', '.', '$', '.', '%', '.', '^', '.', '&']

Number of users: 24
Cluster: 3
[0]
[6, 'A', 'E', 'B', 'F', 'C', '.', 'D']
[5, 'G', 'K', 'H', '.', 'I', '.', 'J']
[5, 'L', 'O', 'M', 'P', 'N', '.']
[4, 'Q', 'T', 'R', '.', 'S', '.']
[4, 'U', 'X', 'V', '.', 'W', '.']
"""


class Cluster:
  def __init__(self, cluster):
    self.name = cluster
    self.spots = CLUSTER_SPOTS[cluster]
    self.filled = 0
    self.rows = []
    row_spots = CLUSTER_ROWS[cluster]
    for i in row_spots:
      self.rows.append(["."] * (i + 1)) #obviously this would be None or sth

def divide_users_to_rows(user_count, cluster):
  user_row_multiplier = user_count / cluster.spots
  users_placed = 0
  for row in cluster.rows:
    row[0] = int(round(user_row_multiplier * (len(row) - 1)))
    users_placed += row[0]
  i = 1
  while users_placed < user_count:
    if (len(cluster.rows[i])) >= 1:
      cluster.rows[i][0] += 1
      users_placed += 1
    i += 2

def place_users(users, cluster): #randomise order of placement? (not necessary)
  for row in cluster.rows:
    if row[0] > 0:
      row_users = users[:row[0]]
      users = users[row[0]:]
      separation = (len(row) - 1) / len(row_users)
      i = 1
      if separation >= 3:
        for user in row_users:
          row[i] = user
          i += 3 #place next user 2 Macs over on the other side if possible
      else:
        for user in row_users:
          row[i] = user
          i += 2
          if (i > len(row) - 1):
            i = 2

def main():
  clusters = []
  for arg in sys.argv[1:]:
    if arg in "123":
      clusters.append(Cluster(int(arg)))
  divide_users_to_rows(len(PH_USERS), clusters[0])
  place_users(PH_USERS, clusters[0])

  #just for visualisation
  print("Number of users:", len(PH_USERS))
  print("Cluster:", clusters[0].name)
  for cluster in clusters: 
    print(*cluster.rows, sep='\n')

if __name__ == "__main__":
  main()