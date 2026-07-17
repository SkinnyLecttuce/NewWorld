// Blueprint used for creating session objects
class Session {
  constructor(id, hostId) {
    this.id = id;
    this.hostId = hostId;
    this.members = new Map();
    this.votes = new Map();
    this.createdAt = Date.now();
  }

  addMembers(socketId, userId, username) {
    this.members.set(socketId, { userId, username });
  }

  removeMembers(socketId) {
    this.members.delete(socketId);
  }

  castVote(movieId, userId) {
    if (!this.votes.has(movieId)) this.votes.set(movieId, new Set());
    this.votes.get(movieId).add(userId);
  }

  getTally() {
    const tally = {};
    for (const [movieId, voters] of this.votes.entries()) {
      tally[movieId] = voters.size;
      return tally;
    }
  }
}


export default Session;