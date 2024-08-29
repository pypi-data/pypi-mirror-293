use surrealdb::Surreal;
use surrealdb::opt::auth::Root;
//use surrealdb::sql::Value;
use surrealdb::engine::remote::ws::Client;
use surrealdb::engine::remote::ws::Ws;
//use std::collections::HashMap;
//use serde_json::Value as JsonValue;
use std::error::Error;
use surrealdb::Response;
//use std::time::Instant;
use pyo3::prelude::*;
//use pyo3::types::PyAny;
use serde::{Deserialize, Serialize};
//use chrono::{DateTime, Utc, Local, NaiveDate, NaiveDateTime, Duration};

#[derive(Debug, Serialize, Deserialize)]
struct UdpTag49 {
    run_counter: u64,
    len_trigger: u16,
    channel: Vec<u8>,
    peak: Vec<u16>,
    peak_position: Vec<u16>,
    position_over: Vec<u16>,
    position_under: Vec<u16>,
    offset_after: Vec<u16>,
    offset_before: Vec<u16>,
    timestamp: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct UdpTag41 {
    run_counter: u64,
    channel: Vec<u8>,
    integral: Vec<u64>,
    mass: Vec<u64>,
    offset: Vec<u16>,
    offset1: Vec<u16>,
    offset2: Vec<u16>,
    tolerance_bottom: Vec<u16>,
    tolerance_top: Vec<u16>,
    project: String,
    timestamp: String,
    status: Vec<Vec<String>>,
}

#[derive(Debug, Serialize, Deserialize)]
struct RawData {
    run_counter: u64,
    channel: u8,
    data: Vec<i32>,
    timestamp: String,
}

// Function to connect to the database
async fn connect_to_db(
    ip: &str,
    port: &str,
    user: &str,
    pw: &str,
    namespace: &str,
    db_name: &str
) -> Result<Surreal<Client>, Box<dyn Error>> {
    let db = Surreal::new::<Ws>(format!("{}:{}", ip, port)).await?;
    db.signin(Root {
        username: &format!("{}", user),
        password: &format!("{}", pw),
    })
    .await?;
    db.use_ns(&format!("{}", namespace)).use_db(&format!("{}", db_name)).await?;
    Ok(db)
}

#[pymodule]
fn sdb_connector(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(select_additional_info_data, m)?)?;
    m.add_function(wrap_pyfunction!(select_measurement_data, m)?)?;
    m.add_function(wrap_pyfunction!(select_raw_data, m)?)?;
    Ok(())
}

#[pyfunction]
fn select_additional_info_data(ip: &str, port: &str,
    user: &str, pw:&str, namespace: &str, db_name: &str,
    table_name: &str, run_id: &str) -> PyResult<Vec<(u64, u16, u8, u16, u16, u16, u16, u16, u16, String)>> {
    // Create a Tokio runtime and block on the async function
    let rt = match tokio::runtime::Runtime::new() {
        Ok(rt) => rt,
        Err(e) => {
            println!("Error creating runtime: {:?}", e);
            return Err(PyErr::new::<pyo3::exceptions::PyException, _>("Error creating runtime"));
        }
    };
    let data = match rt.block_on(select_additional_info_data_async(ip, port,user, pw, namespace, db_name, table_name,run_id)) {
        Ok(data) => data,
        Err(e) => {
            println!("Error selecting additional info data: {:?}", e);
            return Err(PyErr::new::<pyo3::exceptions::PyException, _>("Error selecting additional info data"));
        }
    };
    Ok(data)
}

#[pyfunction]
fn select_measurement_data(ip: &str, port: &str,
    user: &str, pw:&str, namespace: &str, db_name: &str,
    table_name: &str, run_id: &str) -> PyResult<Vec<(u64, u8, u64, u64, u16, u16, u16, u16, u16, String, String, Vec<String>)>> {
    // Create a Tokio runtime and block on the async function
    let rt = match tokio::runtime::Runtime::new() {
        Ok(rt) => rt,
        Err(e) => {
            println!("Error creating runtime: {:?}", e);
            return Err(PyErr::new::<pyo3::exceptions::PyException, _>("Error creating runtime"));
        }
    };
    let data = match rt.block_on(select_measurement_data_async(ip, port,user, pw, namespace, db_name, table_name,run_id)) {
        Ok(data) => data,
        Err(e) => {
            println!("Error selecting measurement data: {:?}", e);
            return Err(PyErr::new::<pyo3::exceptions::PyException, _>("Error selecting measurement data"));
        }
    };
    Ok(data)
}

#[pyfunction]
fn select_raw_data(ip: &str, port: &str,
    user: &str, pw:&str, namespace: &str, db_name: &str,
    table_name: &str, run_id: &str) -> PyResult<Vec<(u64, u8, i32, String)>> {
    // Create a Tokio runtime and block on the async function
    let rt = match tokio::runtime::Runtime::new() {
        Ok(rt) => rt,
        Err(e) => {
            println!("Error creating runtime: {:?}", e);
            return Err(PyErr::new::<pyo3::exceptions::PyException, _>("Error creating runtime"));
        }
    };
    let data = match rt.block_on(select_raw_data_async(ip, port,user, pw, namespace, db_name, table_name,run_id)) {
        Ok(data) => data,
        Err(e) => {
            println!("Error selecting raw data: {:?}", e);
            return Err(PyErr::new::<pyo3::exceptions::PyException, _>("Error selecting raw data"));
        }
    };
    Ok(data)
}

// Function to query data and process it
async fn query_additonal_info_data(
    db: &Surreal<Client>,
    table_name: &str,
    run_id: &str
) -> Result<surrealdb::Response, Box<dyn Error>>{
    let result_query = format!(
        "SELECT run_counter, len_trigger, channel, peak, peak_position, position_over, position_under, offset_after, offset_before, timestamp FROM {} WHERE run_id = {} ORDER BY run_counter ASC",
        table_name, run_id
    );
    let result = db.query(&result_query).await?;
    Ok(result)
}

async fn process_additonal_info_data(result: Response) -> Result<Vec<(u64, u16, u8, u16, u16, u16, u16, u16, u16, String)>, Box<dyn Error>> {
    let mut data = result;
    let data: Vec<UdpTag49> = match data.take(0) {
        Ok(data) => data,
        Err(e) => {
            println!("Error selecting additional info data: {:?}", e);
            return Err(Box::new(e));
        }
    };
    let exploded_data: Vec<(u64, u16, u8, u16, u16, u16, u16, u16, u16, String)> = data
        .into_iter()
        .flat_map(|tag| {
            tag.channel.into_iter()
                .zip(tag.peak.into_iter()) // Combine the channel and peak vectors
                .zip(tag.peak_position.into_iter())
                .zip(tag.position_over.into_iter())
                .zip(tag.position_under.into_iter())
                .zip(tag.offset_after.into_iter())
                .zip(tag.offset_before.into_iter())
                .map(move |((((((channel_value, peak_value), peak_position), position_over), position_under), offset_after), offset_before)| {
                    (tag.run_counter, tag.len_trigger, channel_value, peak_value, peak_position, position_over, position_under, offset_after, offset_before, tag.timestamp.clone())
                })
        })
        .collect();
    Ok(exploded_data)
}

// Main function that uses both helper functions
async fn select_additional_info_data_async(
    ip: &str,
    port: &str,
    user: &str,
    pw: &str,
    namespace: &str,
    db_name: &str,
    table_name: &str,
    run_id: &str
) -> Result<Vec<(u64, u16, u8, u16, u16, u16, u16, u16, u16, String)>, Box<dyn Error>> {
    let db = connect_to_db(ip, port, user, pw, namespace, db_name).await?;
    let result = query_additonal_info_data(&db, table_name, run_id).await?;
    let data = process_additonal_info_data(result).await?;
    Ok(data)
}

// Main function that uses both helper functions
async fn select_measurement_data_async(
    ip: &str,
    port: &str,
    user: &str,
    pw: &str,
    namespace: &str,
    db_name: &str,
    table_name: &str,
    run_id: &str
) -> Result<Vec<(u64, u8, u64, u64, u16, u16, u16, u16, u16, String, String, Vec<String>)>, Box<dyn Error>> {
    let db = connect_to_db(ip, port, user, pw, namespace, db_name).await?;
    let result = query_measurement_data(&db, table_name, run_id).await?;
    let data = process_measurement_data(result).await?;
    Ok(data)
}

pub async fn query_measurement_data(
    db: &Surreal<Client>,
    table_name: &str,
    run_id: &str
) -> Result<surrealdb::Response, Box<dyn Error>>{
    let result_query = format!(
        "SELECT run_counter,channel, integral, mass, offset, offset1, offset2, tolerance_bottom, tolerance_top, project, timestamp, status FROM {} WHERE run_id = {} ORDER BY run_counter ASC",
        table_name, run_id
    );
    let result = db.query(&result_query).await?;
    Ok(result)
}

pub async fn process_measurement_data(result: Response) -> Result<Vec<(u64, u8, u64, u64, u16, u16, u16, u16, u16, String, String, Vec<String>)>, Box<dyn Error>> {
    let mut data = result;
    let data: Vec<UdpTag41> = match data.take(0) {
        Ok(data) => data,
        Err(e) => {
            println!("Error selecting measurement data: {:?}", e);
            return Err(Box::new(e));
        }
    };
    let exploded_data: Vec<(u64, u8, u64, u64, u16, u16, u16, u16, u16, String, String, Vec<String>)> = data
        .into_iter()
        .flat_map(|tag| {
            tag.channel.into_iter()
                .zip(tag.integral.into_iter()) // Combine the channel and peak vectors
                .zip(tag.mass.into_iter())
                .zip(tag.offset.into_iter())
                .zip(tag.offset1.into_iter())
                .zip(tag.offset2.into_iter())
                .zip(tag.tolerance_bottom.into_iter())
                .zip(tag.tolerance_top.into_iter())
                .zip(tag.status.clone().into_iter())
                .map(move |((((((((channel_value, integral), mass), offset), offset1), offset2), tolerance_bottom), tolerance_top), status)| {
                    (tag.run_counter, channel_value, integral, mass, offset, offset1, offset2, tolerance_bottom, tolerance_top, tag.project.clone(), tag.timestamp.clone(),status)
                })
        })
        .collect();
    Ok(exploded_data)
}

// Main function that uses both helper functions
async fn select_raw_data_async(
    ip: &str,
    port: &str,
    user: &str,
    pw: &str,
    namespace: &str,
    db_name: &str,
    table_name: &str,
    run_id: &str
) -> Result<Vec<(u64, u8, i32, String)>, Box<dyn Error>> {
    let db = connect_to_db(ip, port, user, pw, namespace, db_name).await?;
    let result = query_raw_data(&db, table_name, run_id).await?;
    let data = process_raw_data(result).await?;
    Ok(data)
}

pub async fn query_raw_data(
    db: &Surreal<Client>,
    table_name: &str,
    run_id: &str
) -> Result<surrealdb::Response, Box<dyn Error>>{
    let result_query = format!(
        "SELECT run_counter,channel, data, timestamp FROM {} WHERE run_id = {} ORDER BY run_counter ASC",
        table_name, run_id
    );
    let result = db.query(&result_query).await?;
    Ok(result)
}


pub async fn process_raw_data(result: Response) -> Result<Vec<(u64, u8, i32, String)>, Box<dyn Error>> {
    let mut ddata = result;
    let data: Vec<RawData> = match ddata.take(0) {
        Ok(data) => data,
        Err(e) => {
            println!("Error selecting raw data: {:?}", e);
            return Err(Box::new(e));
        }
    };
    let mut exploded_data = Vec::new();
        
    for tag in data {
            let channel_value = tag.channel;
            let run_counter = tag.run_counter;
            let timestamp = tag.timestamp;
            
            for data_value in tag.data {
                exploded_data.push((run_counter, channel_value, data_value, timestamp.clone()));
            }
        }
        
        Ok(exploded_data)
}
    


    