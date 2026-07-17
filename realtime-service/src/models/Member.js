// Blueprint used for creating member objects
class Member {
    constructor(socketId, userId, username) {
        this.socketId = socketId;
        this.userId = userId;
        this.username = username;
        this.joinedAt = Date.now();
    }
}

export default Member;