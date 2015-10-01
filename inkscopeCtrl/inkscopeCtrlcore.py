# Alpha O. Sall
# Alain Dechorgnat
# 03/24/2014

from flask import Flask, Response
from subprocess import CalledProcessError
app = Flask(__name__)  # ,template_folder='/var/www/inkscope/inkscopeAdm/')

import mongoJuiceCore

import poolsCtrl
import osdsCtrl
import rbdCtrl

from S3Ctrl import S3Ctrl, S3Error
from S3ObjectCtrl import *


# Load configuration from file
configfile = "/opt/inkscope/etc/inkscope.conf"
datasource = open(configfile, "r")
conf = json.load(datasource)
datasource.close()


#
# mongoDB query facility
#
@app.route('/<db>/<collection>', methods=['GET', 'POST'])
def find(db, collection):
    return mongoJuiceCore.find(conf, db, collection)


@app.route('/<db>', methods=['POST'])
def full(db):
    return mongoJuiceCore.full(conf, db)


#
# global management
#
@app.route('/conf.json', methods=['GET'])
def conf_manage():
    platform = conf.get("platform")
    result = json.dumps({"platform": platform})
    return Response(result, mimetype='application/json')


#
# Pools management
#
@app.route('/poolList/', methods=['GET'])
def pool_list():
    return Response(poolsCtrl.pool_list(), mimetype='application/json')


@app.route('/pools/', methods=['GET', 'POST'])
@app.route('/pools/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def pool_manage(id=None):
    return poolsCtrl.pool_manage(id)


@app.route('/pools/<int:id>/snapshot', methods=['POST'])
def makesnapshot(id):
    return poolsCtrl.makesnapshot(id)


@app.route('/pools/<int:id>/snapshot/<namesnapshot>', methods=['DELETE'])
def removesnapshot(id, namesnapshot):
    return poolsCtrl.removesnapshot(id, namesnapshot)


#
# RBD management
#
#
# Images
#
@app.route('/RBD/images', methods=['GET'])
def getImagesList():
    # Log.debug("Calling  rbdCtrl.listImages() method")
    try:
        return Response(rbdCtrl.list_images(), mimetype='application/json')
    except CalledProcessError, e:
        return Response(e.output, status=500)

@app.route('/RBD/images/<string:pool_name>/<string:image_name>', methods=['GET'])
def getImagesInfo(pool_name, image_name):
    # Log.debug("Calling  rbdCtrl.getImagesInfo() method")
    try:
        return Response(rbdCtrl.image_info(pool_name, image_name), mimetype='application/json')
    except CalledProcessError, e:
        return Response(e.output, status=500)

@app.route('/RBD/images/<string:pool_name>/<string:image_name>', methods=['PUT'])
def createImage(pool_name, image_name):
    # Log.debug("Calling  rbdCtrl.listImages() method")
    try:
        return Response(rbdCtrl.create_image(pool_name, image_name), mimetype='application/json')
    except CalledProcessError, e:
        return Response(e.output, status=500)


@app.route('/RBD/images/<string:pool_name>/<string:image_name>/<string:action>', methods=['POST'])
def modifyImage(pool_name, image_name , action):
    # Log.debug("Calling  rbdCtrl.modifyImages() method")
    try:
        return Response(rbdCtrl.modify_image(pool_name, image_name, action), mimetype='application/json')
    except CalledProcessError, e:
        return Response(e.output, status=500)


@app.route('/RBD/images/<string:pool_name>/<string:image_name>', methods=['DELETE'])
def deleteImage(pool_name, image_name):
    # Log.debug("Calling  rbdCtrl.deleteImage() method")
    try:
        return Response(rbdCtrl.delete_image(pool_name, image_name), mimetype='application/json')
    except CalledProcessError, e:
        return Response(e.output, status=500)


#
# Snapshots
#
@app.route('/RBD/snapshots/<string:pool_name>/<string:image_name>/<string:snap_name>', methods=['GET'])
def infoImageSnapshot(pool_name, image_name,snap_name):
    # Log.debug("Calling  rbdCtrl.info_image_snapshot() method")
    try:
        return Response(rbdCtrl.info_image_snapshot(pool_name, image_name, snap_name), mimetype='application/json')
    except CalledProcessError, e:
        return Response(e.output, status=500)


@app.route('/RBD/snapshots/<string:pool_name>/<string:image_name>/<string:snap_name>', methods=['PUT'])
def createImageSnapshot(pool_name, image_name,snap_name):
    # Log.debug("Calling  rbdCtrl.create_image_snapshot() method")
    try:
        return Response(rbdCtrl.create_image_snapshot(pool_name, image_name, snap_name), mimetype='application/json')
    except CalledProcessError, e:
        return Response(e.output, status=500)


@app.route('/RBD/snapshots/<string:pool_name>/<string:image_name>/<string:snap_name>', methods=['DELETE'])
def deleteImageSnapshot(pool_name, image_name,snap_name):
    # Log.debug("Calling  rbdCtrl.delete_image_snapshot() method")
    try:
        return Response(rbdCtrl.delete_image_snapshot(pool_name, image_name, snap_name), mimetype='application/json')
    except CalledProcessError, e:
        return Response(e.output, status=500)


@app.route('/RBD/snapshots/<string:pool_name>/<string:image_name>/<string:snap_name>/<string:action>', methods=['POST'])
def actionOnImageSnapshot(pool_name, image_name,snap_name, action):
    # print "Calling  rbdCtrl.action_on_image_snapshot() method", action
    try:
        return Response(rbdCtrl.action_on_image_snapshot(pool_name, image_name, snap_name, action), mimetype='application/json')
    except CalledProcessError, e:
        return Response(e.output, status=500)


#
# Osds management
#

@app.route('/osds', methods=['PUT'])
def osds_manage(id=None):
    return osdsCtrl.osds_manage(id)


#
# Object storage management
#
# This method return a S3 Object that id is "objId".
# An exception is trhown if the object does not exist or there an issue
@app.route('/S3/object', methods=['GET'])
def getObjectStructure():
    Log.debug("Calling  getObjectStructure() method")
    try:
        return Response(S3ObjectCtrl(conf).getObjectStructure(),mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)

# User management
@app.route('/S3/user', methods=['GET'])
def listUser():
    try:
        return Response(S3Ctrl(conf).listUsers(),mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)

@app.route('/S3/user', methods=['POST'])
def createUser():
    try:
        return Response(S3Ctrl(conf).createUser(),mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)

@app.route('/S3/user/<string:uid>', methods=['GET'])
def getUser(uid):
    try:
        return Response(S3Ctrl(conf).getUser(uid),mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)

@app.route('/S3/user/<string:uid>', methods=['PUT'])
def modifyUser(uid):
    try:
        return Response(S3Ctrl(conf).modifyUser(uid),mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)

@app.route('/S3/user/<string:uid>', methods=['DELETE'])
def removeUser(uid):
    try:
        return Response(S3Ctrl(conf).removeUser(uid),mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)


@app.route('/S3/user/<string:uid>/key/<string:key>', methods=['DELETE'])
def removeUserKey(uid,key):
    try:
        return Response(S3Ctrl(conf).removeUserKey(uid,key),mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)

@app.route('/S3/user/<string:uid>/subuser', methods=['PUT'])
def createSubuser(uid):
    try:
        return Response(S3Ctrl(conf).createSubuser(uid),mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)

@app.route('/S3/user/<string:uid>/subuser/<string:subuser>', methods=['DELETE'])
def deleteSubuser(uid, subuser):
    try:
        return Response(S3Ctrl(conf).deleteSubuser(uid, subuser),mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)


@app.route('/S3/user/<string:uid>/subuser/<string:subuser>/key', methods=['PUT'])
def createSubuserKey(uid, subuser):
    Log.debug("createSubuserKey")
    try:
        return Response(S3Ctrl(conf).createSubuserKey(uid, subuser),mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)

@app.route('/S3/user/<string:uid>/subuser/<string:subuser>/key/<string:key>', methods=['DELETE'])
def deleteSubuserKey(uid, subuser, key):
    Log.debug("deleteSubuserKey")
    try:
        return Response(S3Ctrl(conf).deleteSubuserKey(uid, subuser,key),mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)

@app.route('/S3/user/<string:uid>/caps', methods=['PUT', 'POST'])
def saveCapability(uid):
    Log.debug("saveCapability")
    try:
        return Response(S3Ctrl(conf).saveCapability(uid),mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)

@app.route('/S3/user/<string:uid>/caps', methods=['DELETE'])
def deleteCapability(uid):
    Log.debug("deleteCapability")
    try:
        return Response(S3Ctrl(conf).deleteCapability(uid),mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)

# bucket management

@app.route('/S3/user/<string:uid>/buckets', methods=['GET'])
def getUserBuckets(uid,bucket=None):
    try:
        return Response(S3Ctrl(conf).getUserBuckets(uid),mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)


@app.route('/S3/bucket', methods=['PUT'])
def createBucket():
    try:
        return Response(S3Ctrl(conf).createBucket(), mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)


@app.route('/S3/bucket', methods=['GET'])
def getBuckets():
    try:
        return Response(S3Ctrl(conf).getBucketInfo(None), mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)

@app.route('/S3/bucket/<string:bucket>', methods=['GET'])
def getBucketInfo(bucket=None):
    try:
        return Response(S3Ctrl(conf).getBucketInfo(bucket), mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)

@app.route('/S3/bucket/<string:bucket>', methods=['DELETE'])
def deleteBucket(bucket):
    try:
        return Response(S3Ctrl(conf).deleteBucket(bucket), mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)

@app.route('/S3/bucket/<string:bucket>/link', methods=['DELETE','PUT'])
def linkBucket(bucket):
    try:
        uid = request.form['uid']
        if request.method =='PUT':
            return Response(S3Ctrl(conf).linkBucket(uid, bucket), mimetype='application/json')
        else:
            return Response(S3Ctrl(conf).unlinkBucket(uid, bucket), mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)

@app.route('/S3/bucket/<string:bucketName>/list', methods=['GET'])
def listBucket(bucketName):
    try:
        return Response(S3Ctrl(conf).listBucket(bucketName), mimetype='application/json')
    except S3Error , e:
        Log.err(e.__str__())
        return Response(e.reason, status=e.code)

