import org.apache.spark.mllib.linalg.Vectors

import org.apache.spark.mllib.clustering.KMeans
import scala.io.Source
import org.apache.spark.sql.functions._

//For batsman

    val data = sc.textFile("hdfs://localhost:9000/user/batman/ipl/op/op1/bat_only")

    // comma separator split
    val rows = data.map(line => line.split(","))

    // define case class
    case class CC1(role: String,batsman_name: String, avgScore: Double, avgStrikeRate: Double,totalMatches: Int)

    // map parts to case class
    val allData = rows.map( p => CC1(p(0).toString, p(1).toString, p(2).trim.toDouble,  p(3).trim.toDouble, p(4).trim.toInt))

    // convert rdd to dataframe
    val allDF = allData.toDF()

    // convert back to rdd and cache the data
    val rowsRDD = allDF.rdd.map(r => (r.getString(0),r.getString(1), r.getDouble(2), r.getDouble(3),r.getInt(4) ))
    rowsRDD.cache()

    // convert data to RDD which will be passed to KMeans and cache the data. These are the attributes we want to use to assign the instance to a cluster
    val vectors = allDF.rdd.map(r => Vectors.dense( r.getDouble(2),r.getDouble(3),r.getInt(4)))
    vectors.cache()

    //KMeans model with 2 clusters and 20 iterations
    val kMeansModel = KMeans.train(vectors, 6, 20)

    // Get the prediction from the model with the ID so we can link them back to other information
    //maps each data roow with its cluster index it belongs to. 

    val predictions = rowsRDD.map(r => (r._2, kMeansModel.predict(Vectors.dense(r._3,r._4,r._5))))

    // convert the rdd to a dataframe
    val predDF = predictions.toDF("batsman_name", "CLUSTER")
    val finalDF = allDF.join(predDF,"batsman_name")
    //Print the center of each cluster
    kMeansModel.clusterCenters.foreach(println)

//For bowlers
    val data1 = sc.textFile("hdfs://localhost:9000/user/batman/ipl/op/op1/bowl_only")

    // comma separator split
    val rows1 = data1.map(line => line.split(","))

    // define case class
    case class CC2(role: String,bowler_name: String, bowlAvg: Double, economy: Double,bowlStrike: Double,totalMatches: Int)

    // map parts to case class
    val allData1 = rows1.map( p => CC2(p(0).toString, p(1).toString, p(2).trim.toDouble,  p(3).trim.toDouble, p(4).trim.toDouble, p(5).trim.toInt))

    // convert rdd to dataframe
    val allDF1 = allData1.toDF()

    // convert back to rdd and cache the data
    val rowsRDD1 = allDF1.rdd.map(r => (r.getString(0),r.getString(1), r.getDouble(2), r.getDouble(3),r.getDouble(4),r.getInt(5) ))
    rowsRDD1.cache()

    // convert data to RDD which will be passed to KMeans and cache the data. These are the attributes we want to use to assign the instance to a cluster
    val vectors1 = allDF1.rdd.map(r => Vectors.dense( r.getDouble(2),r.getDouble(3),r.getDouble(4),r.getInt(5)))
    vectors1.cache()

    //KMeans model with 2 clusters and 20 iterations
    val kMeansModel1 = KMeans.train(vectors1, 6, 20)

    // Get the prediction from the model with the ID so we can link them back to other information
    //maps each data roow with its cluster index it belongs to. 

    val predictions1 = rowsRDD1.map(r => (r._2, kMeansModel1.predict(Vectors.dense(r._3,r._4,r._5,r._6))))

    // convert the rdd to a dataframe
    val predDF1 = predictions1.toDF("bowler_name", "CLUSTER")
    val finalDF1 = allDF1.join(predDF1,"bowler_name")
    //Print the center of each cluster
    kMeansModel1.clusterCenters.foreach(println)
