// pages/verification/verification.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    time: 60,
    timestate: 0
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {

  },
  onConfirm:function(){
    wx.navigateTo({
      url: '/pages/result/result',
     
    })
  } ,
  onObtain: function() {
    var that = this;
    var count = this.data.time;
    setTimeout(function() {
      count--;
      console.log(count)
      that.onObtain();
      that.setData({
        time: count

      })
    }, 1000);
    that.setData({
      timestate: 1,
    })


  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  }
})